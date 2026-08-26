// SmartKYC Frontend Controller & State Manager
let currentUser = null;
let distChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    setupEventListeners();
});

// --- Auth State & Session Check ---
async function checkAuth() {
    try {
        const res = await fetch('/api/auth/me');
        if (res.ok) {
            currentUser = await res.json();
            renderAuthenticatedApp();
        } else {
            renderLoginScreen();
        }
    } catch (err) {
        renderLoginScreen();
    }
}

function renderLoginScreen() {
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('app-screen').style.display = 'none';
}

function renderAuthenticatedApp() {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app-screen').style.display = 'flex';
    
    // Update user info banner
    document.getElementById('user-display-name').textContent = currentUser.full_name || currentUser.username;
    document.getElementById('user-display-role').textContent = currentUser.role;
    
    // RBAC: Show/hide Admin items
    const adminNavs = document.querySelectorAll('.admin-only');
    adminNavs.forEach(el => {
        el.style.display = (currentUser.role === 'Admin') ? 'flex' : 'none';
    });
    
    switchTab('dashboard');
}

// --- Tab Switching Navigation ---
function switchTab(tabName) {
    document.querySelectorAll('.tab-pane').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    
    const targetPane = document.getElementById(`tab-${tabName}`);
    const targetNav = document.getElementById(`nav-${tabName}`);
    
    if (targetPane) targetPane.style.display = 'block';
    if (targetNav) targetNav.classList.add('active');
    
    // Close mobile sidebar on navigation
    document.querySelector('.sidebar').classList.remove('open');
    
    if (tabName === 'dashboard') loadDashboard();
    if (tabName === 'history') loadHistory();
    if (tabName === 'users') loadUsers();
    if (tabName === 'audit') loadAuditLogs();
}

// --- Event Listeners Setup ---
function setupEventListeners() {
    // Login Form Submit
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value;
            const errorBox = document.getElementById('login-error');
            errorBox.style.display = 'none';
            
            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                if (res.ok) {
                    currentUser = await res.json();
                    renderAuthenticatedApp();
                } else {
                    const data = await res.json();
                    errorBox.textContent = data.detail || 'Invalid username or password.';
                    errorBox.style.display = 'block';
                }
            } catch (err) {
                errorBox.textContent = 'Connection error. Please try again.';
                errorBox.style.display = 'block';
            }
        });
    }
    
    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            await fetch('/api/auth/logout', { method: 'POST' });
            currentUser = null;
            renderLoginScreen();
        });
    }
    
    // PAN Validation Form
    const panForm = document.getElementById('pan-form');
    if (panForm) {
        panForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const panNumber = document.getElementById('pan-input').value.trim();
            const resultBox = document.getElementById('pan-result');
            
            resultBox.innerHTML = `<div style="color: #94a3b8;">Verifying PAN format...</div>`;
            resultBox.style.display = 'block';
            
            const res = await fetch('/api/validate/pan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pan_number: panNumber })
            });
            const data = await res.json();
            renderValidationResult(resultBox, data, 'PAN');
        });
    }
    
    // Aadhaar Validation Form
    const aadhaarForm = document.getElementById('aadhaar-form');
    if (aadhaarForm) {
        aadhaarForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const aadhaarNumber = document.getElementById('aadhaar-input').value.trim();
            const resultBox = document.getElementById('aadhaar-result');
            
            resultBox.innerHTML = `<div style="color: #94a3b8;">Calculating Verhoeff checksum...</div>`;
            resultBox.style.display = 'block';
            
            const res = await fetch('/api/validate/aadhaar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ aadhaar_number: aadhaarNumber })
            });
            const data = await res.json();
            renderValidationResult(resultBox, data, 'Aadhaar');
        });
    }
    
    // Create User Form (Admin)
    const createUserForm = document.getElementById('create-user-form');
    if (createUserForm) {
        createUserForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                full_name: document.getElementById('new-user-fullname').value,
                username: document.getElementById('new-user-username').value,
                email: document.getElementById('new-user-email').value,
                phone: document.getElementById('new-user-phone').value,
                role: document.getElementById('new-user-role').value,
                password: document.getElementById('new-user-password').value
            };
            
            const res = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (res.ok) {
                alert('User created successfully!');
                createUserForm.reset();
                loadUsers();
            } else {
                const err = await res.json();
                alert(err.detail || 'Failed to create user.');
            }
        });
    }
    
    // Mobile Sidebar Toggle
    const toggleBtn = document.getElementById('mobile-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.querySelector('.sidebar').classList.toggle('open');
        });
    }
}

// --- Render Validation Results ---
function renderValidationResult(container, data, type) {
    if (data.valid) {
        let detailsHtml = '';
        if (data.details) {
            if (type === 'PAN') {
                detailsHtml = `
                    <div style="margin-top: 10px; font-size: 0.88rem; color: #cbd5e1;">
                        <div>• <b>Entity Category:</b> ${data.details.entity_type} (Code: ${data.details.entity_code})</div>
                        <div>• <b>Surname Initial:</b> ${data.details.surname_initial}</div>
                    </div>
                `;
            } else if (type === 'Aadhaar') {
                detailsHtml = `
                    <div style="margin-top: 10px; font-size: 0.88rem; color: #cbd5e1;">
                        <div>• <b>Formatted UID:</b> <code>${data.details.formatted}</code></div>
                        <div>• <b>Algorithm:</b> ${data.details.algorithm} (Passed)</div>
                    </div>
                `;
            }
        }
        
        container.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #34d399; font-size: 1.1rem;">✓</span>
                    <strong style="color: #34d399; font-size: 1rem;">VALID ${type} DOCUMENT</strong>
                </div>
                <p style="margin-top: 6px; color: #e2e8f0; font-size: 0.9rem;">${data.reason}</p>
                ${detailsHtml}
            </div>
        `;
    } else {
        container.innerHTML = `
            <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 10px; padding: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #fb7185; font-size: 1.1rem;">✕</span>
                    <strong style="color: #fb7185; font-size: 1rem;">INVALID ${type} DOCUMENT</strong>
                </div>
                <p style="margin-top: 6px; color: #fecdd3; font-size: 0.9rem;">${data.reason}</p>
            </div>
        `;
    }
}

// --- Load Dashboard Data ---
async function loadDashboard() {
    try {
        const res = await fetch('/api/dashboard/stats');
        if (!res.ok) return;
        const stats = await res.json();
        
        document.getElementById('kpi-total').textContent = stats.total_validations;
        document.getElementById('kpi-valid').textContent = stats.valid_count;
        document.getElementById('kpi-invalid').textContent = stats.invalid_count;
        document.getElementById('kpi-rate').textContent = `${stats.success_rate}%`;
        
        // Render Chart
        renderDistributionChart(stats.valid_count, stats.invalid_count);
        
        // Render Recent Table
        const tbody = document.getElementById('recent-table-body');
        tbody.innerHTML = '';
        stats.recent_validations.forEach(r => {
            const tr = document.createElement('tr');
            const badgeClass = (r.status === 'VALID') ? 'badge-valid' : 'badge-invalid';
            const dateStr = new Date(r.validated_at).toLocaleString();
            tr.innerHTML = `
                <td><strong>${r.document_type}</strong></td>
                <td><code>${r.document_number}</code></td>
                <td><span class="badge ${badgeClass}">${r.status}</span></td>
                <td style="color: #64748b; font-size: 0.85rem;">${dateStr}</td>
                <td>${r.validated_by || 'System'}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
    }
}

function renderDistributionChart(valid, invalid) {
    const ctx = document.getElementById('distributionChart');
    if (!ctx) return;
    
    if (distChart) distChart.destroy();
    
    distChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Valid Documents', 'Invalid Checks'],
            datasets: [{
                data: [valid, invalid],
                backgroundColor: ['#10b981', '#f43f5e'],
                borderColor: '#111827',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } } }
            }
        }
    });
}


// --- Load History Data ---
async function loadHistory() {
    const search = document.getElementById('history-search')?.value || '';
    const docType = document.getElementById('history-type')?.value || '';
    const status = document.getElementById('history-status')?.value || '';
    
    let url = `/api/history?limit=100`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (docType) url += `&doc_type=${encodeURIComponent(docType)}`;
    if (status) url += `&status=${encodeURIComponent(status)}`;
    
    const res = await fetch(url);
    if (!res.ok) return;
    const records = await res.json();
    
    const tbody = document.getElementById('history-table-body');
    tbody.innerHTML = '';
    records.forEach(r => {
        const tr = document.createElement('tr');
        const badgeClass = (r.status === 'VALID') ? 'badge-valid' : 'badge-invalid';
        tr.innerHTML = `
            <td>#${r.validation_id}</td>
            <td><strong>${r.document_type}</strong></td>
            <td><code>${r.document_number}</code></td>
            <td><span class="badge ${badgeClass}">${r.status}</span></td>
            <td style="color: #cbd5e1; font-size: 0.85rem;">${r.failure_reason || '—'}</td>
            <td style="color: #94a3b8; font-size: 0.85rem;">${new Date(r.validated_at).toLocaleString()}</td>
            <td>${r.validated_by}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Load Users (Admin) ---
async function loadUsers() {
    const res = await fetch('/api/users');
    if (!res.ok) return;
    const users = await res.json();
    
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = '';
    users.forEach(u => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${u.username}</strong></td>
            <td>${u.full_name}</td>
            <td>${u.email}</td>
            <td><span class="badge badge-role">${u.role}</span></td>
            <td><span style="color: #34d399;">🟢 ${u.status}</span></td>
            <td>
                ${u.user_id !== currentUser.user_id ? 
                    `<button class="btn-danger" onclick="deleteUserAccount(${u.user_id}, '${u.username}')">Delete</button>` 
                    : '<span style="color: #94a3b8; font-size: 0.85rem;">(Active Admin)</span>'}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteUserAccount(userId, username) {
    if (!confirm(`Are you sure you want to permanently delete user '${username}'?`)) return;
    
    const res = await fetch(`/api/users/${userId}`, { method: 'DELETE' });
    if (res.ok) {
        alert(`User '${username}' deleted.`);
        loadUsers();
    } else {
        const err = await res.json();
        alert(err.detail || 'Delete failed.');
    }
}

// --- Load Audit Logs (Admin) ---
async function loadAuditLogs() {
    const res = await fetch('/api/audit?limit=100');
    if (!res.ok) return;
    const logs = await res.json();
    
    const tbody = document.getElementById('audit-table-body');
    tbody.innerHTML = '';
    logs.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${l.log_id}</td>
            <td><code>${l.action}</code></td>
            <td><span class="badge badge-role">${l.module}</span></td>
            <td style="color: #e2e8f0; font-size: 0.9rem;">${l.description || '—'}</td>
            <td style="color: #94a3b8; font-size: 0.85rem;">${new Date(l.timestamp).toLocaleString()}</td>
            <td><strong>${l.performed_by}</strong></td>
        `;
        tbody.appendChild(tr);
    });
}
