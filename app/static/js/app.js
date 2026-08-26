/**
 * SmartKYC Enterprise Client-Side MVC Controller & State Engine
 * Handles session tokens, reactive DOM rendering, debounce filtering, and toast notifications.
 */

let currentUser = null;
let distChart = null;
let historyDebounceTimer = null;

document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    setupEventListeners();
    setupInputFormatters();
});

// --- Toast Notification Engine ---
function showToast(type, message) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let iconSvg = '';
    if (type === 'success') {
        iconSvg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`;
    } else if (type === 'error') {
        iconSvg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
    } else {
        iconSvg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`;
    }
    
    toast.innerHTML = `${iconSvg} <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

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
    
    document.getElementById('user-display-name').textContent = currentUser.full_name || currentUser.username;
    document.getElementById('user-display-role').textContent = currentUser.role;
    
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
    
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.remove('open');
    
    if (tabName === 'dashboard') loadDashboard();
    if (tabName === 'history') loadHistory();
    if (tabName === 'users') loadUsers();
    if (tabName === 'audit') loadAuditLogs();
}

// --- Live Input Formatters ---
function setupInputFormatters() {
    const aadhaarInput = document.getElementById('aadhaar-input');
    if (aadhaarInput) {
        aadhaarInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '');
            if (val.length > 12) val = val.substring(0, 12);
            const chunks = val.match(/.{1,4}/g);
            e.target.value = chunks ? chunks.join(' ') : val;
        });
    }

    const panInput = document.getElementById('pan-input');
    if (panInput) {
        panInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }
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
                    showToast('success', `Authenticated as ${currentUser.username}`);
                    renderAuthenticatedApp();
                } else {
                    const data = await res.json();
                    errorBox.textContent = data.detail || 'Invalid credentials.';
                    errorBox.style.display = 'block';
                }
            } catch (err) {
                errorBox.textContent = 'Service unavailable. Please retry.';
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
            showToast('info', 'Signed out of session');
            renderLoginScreen();
        });
    }
    
    // PAN Form
    const panForm = document.getElementById('pan-form');
    if (panForm) {
        panForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const panNumber = document.getElementById('pan-input').value.trim();
            const resultBox = document.getElementById('pan-result');
            
            resultBox.innerHTML = `<div style="color: #64748b; font-size: 0.85rem;">Processing format validation...</div>`;
            resultBox.style.display = 'block';
            
            const startTime = performance.now();
            const res = await fetch('/api/validate/pan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pan_number: panNumber })
            });
            const latency = (performance.now() - startTime).toFixed(1);
            const data = await res.json();
            renderValidationResult(resultBox, data, 'PAN', latency);
        });
    }
    
    // Aadhaar Form
    const aadhaarForm = document.getElementById('aadhaar-form');
    if (aadhaarForm) {
        aadhaarForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const aadhaarNumber = document.getElementById('aadhaar-input').value.trim();
            const resultBox = document.getElementById('aadhaar-result');
            
            resultBox.innerHTML = `<div style="color: #64748b; font-size: 0.85rem;">Calculating Dihedral Group matrix...</div>`;
            resultBox.style.display = 'block';
            
            const startTime = performance.now();
            const res = await fetch('/api/validate/aadhaar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ aadhaar_number: aadhaarNumber })
            });
            const latency = (performance.now() - startTime).toFixed(1);
            const data = await res.json();
            renderValidationResult(resultBox, data, 'Aadhaar', latency);
        });
    }
    
    // Create User Form
    const createUserForm = document.getElementById('create-user-form');
    if (createUserForm) {
        createUserForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                full_name: document.getElementById('new-user-fullname').value.trim(),
                username: document.getElementById('new-user-username').value.trim(),
                email: document.getElementById('new-user-email').value.trim(),
                phone: document.getElementById('new-user-phone').value.trim() || null,
                role: document.getElementById('new-user-role').value,
                password: document.getElementById('new-user-password').value
            };
            
            const res = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (res.ok) {
                showToast('success', `Operator account '${payload.username}' provisioned.`);
                createUserForm.reset();
                loadUsers();
            } else {
                const err = await res.json();
                showToast('error', err.detail || 'Failed to create account.');
            }
        });
    }

    // Debounced History Search
    const searchInput = document.getElementById('history-search');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(historyDebounceTimer);
            historyDebounceTimer = setTimeout(loadHistory, 250);
        });
    }
    
    const typeSelect = document.getElementById('history-type');
    if (typeSelect) typeSelect.addEventListener('change', loadHistory);

    const statusSelect = document.getElementById('history-status');
    if (statusSelect) statusSelect.addEventListener('change', loadHistory);
    
    // Mobile Sidebar Toggle
    const toggleBtn = document.getElementById('mobile-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.querySelector('.sidebar').classList.toggle('open');
        });
    }
}

// --- Render Validation Results ---
function renderValidationResult(container, data, type, latency) {
    if (data.valid) {
        let specHtml = '';
        if (data.details) {
            if (type === 'PAN') {
                specHtml = `
                    <div class="spec-grid">
                        <div class="spec-item">
                            <div class="spec-key">Entity Category</div>
                            <div class="spec-val">${data.details.entity_type} (${data.details.entity_code})</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Surname Marker</div>
                            <div class="spec-val font-mono">${data.details.surname_initial}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Protocol</div>
                            <div class="spec-val font-mono">ITD-Sec 139A</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Verification Latency</div>
                            <div class="spec-val font-mono">${latency} ms</div>
                        </div>
                    </div>
                `;
            } else if (type === 'Aadhaar') {
                specHtml = `
                    <div class="spec-grid">
                        <div class="spec-item">
                            <div class="spec-key">Formatted UID</div>
                            <div class="spec-val font-mono">${data.details.formatted}</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Algorithm</div>
                            <div class="spec-val">Verhoeff D5 Checksum</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Standard</div>
                            <div class="spec-val font-mono">ISO/IEC 7064</div>
                        </div>
                        <div class="spec-item">
                            <div class="spec-key">Verification Latency</div>
                            <div class="spec-val font-mono">${latency} ms</div>
                        </div>
                    </div>
                `;
            }
        }
        
        container.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                        <strong style="color: #34d399; font-size: 0.95rem;">VERIFIED ${type} DOCUMENT</strong>
                    </div>
                    <span class="badge badge-valid">200 VALID</span>
                </div>
                <p style="margin-top: 6px; color: #94a3b8; font-size: 0.85rem;">${data.reason}</p>
                ${specHtml}
            </div>
        `;
    } else {
        container.innerHTML = `
            <div style="background: rgba(244, 63, 94, 0.06); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 8px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                        <strong style="color: #fb7185; font-size: 0.95rem;">REJECTED ${type} DOCUMENT</strong>
                    </div>
                    <span class="badge badge-invalid">422 INVALID</span>
                </div>
                <p style="margin-top: 6px; color: #fecdd3; font-size: 0.85rem;">${data.reason}</p>
                <div style="margin-top: 8px; font-size: 0.75rem; color: #64748b; font-family: 'JetBrains Mono', monospace;">Processed in ${latency} ms</div>
            </div>
        `;
    }
}

// --- Load Dashboard Telemetry ---
async function loadDashboard() {
    try {
        const res = await fetch('/api/dashboard/stats');
        if (!res.ok) return;
        const stats = await res.json();
        
        document.getElementById('kpi-total').textContent = stats.total_validations;
        document.getElementById('kpi-valid').textContent = stats.valid_count;
        document.getElementById('kpi-invalid').textContent = stats.invalid_count;
        document.getElementById('kpi-rate').textContent = `${stats.success_rate}%`;
        
        renderDistributionChart(stats.valid_count, stats.invalid_count);
        
        const tbody = document.getElementById('recent-table-body');
        tbody.innerHTML = '';
        if (stats.recent_validations.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #64748b; padding: 20px;">No validations recorded yet.</td></tr>`;
            return;
        }
        
        stats.recent_validations.forEach(r => {
            const tr = document.createElement('tr');
            const badgeClass = (r.status === 'VALID') ? 'badge-valid' : 'badge-invalid';
            const dateStr = new Date(r.validated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            tr.innerHTML = `
                <td><span style="font-weight: 600; color: #f8fafc;">${r.document_type}</span></td>
                <td><code class="font-mono">${r.document_number}</code></td>
                <td><span class="badge ${badgeClass}">${r.status}</span></td>
                <td style="color: #64748b; font-size: 0.82rem;" class="font-mono">${dateStr}</td>
                <td><span style="color: #94a3b8; font-size: 0.85rem;">${r.validated_by || 'System'}</span></td>
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
            labels: ['Verified Valid', 'Integrity Failures'],
            datasets: [{
                data: [valid, invalid],
                backgroundColor: ['#10b981', '#f43f5e'],
                borderColor: '#131b2e',
                borderWidth: 3,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'bottom', 
                    labels: { 
                        color: '#94a3b8', 
                        font: { family: 'Inter', size: 11, weight: '500' },
                        boxWidth: 10,
                        padding: 14
                    } 
                }
            },
            cutout: '70%'
        }
    });
}

// --- Load History Registry ---
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
    
    if (records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #64748b; padding: 24px;">No matching records found in audit ledger.</td></tr>`;
        return;
    }
    
    records.forEach(r => {
        const tr = document.createElement('tr');
        const badgeClass = (r.status === 'VALID') ? 'badge-valid' : 'badge-invalid';
        tr.innerHTML = `
            <td class="font-mono" style="color: #64748b;">#${r.validation_id}</td>
            <td><strong>${r.document_type}</strong></td>
            <td><code class="font-mono">${r.document_number}</code></td>
            <td><span class="badge ${badgeClass}">${r.status}</span></td>
            <td style="color: #94a3b8; font-size: 0.82rem;">${r.reason || 'Verification passed'}</td>
            <td style="color: #64748b; font-size: 0.8rem;" class="font-mono">${new Date(r.validated_at).toLocaleString()}</td>
            <td style="color: #94a3b8;">${r.validated_by}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Load Users Directory ---
async function loadUsers() {
    const res = await fetch('/api/users');
    if (!res.ok) return;
    const users = await res.json();
    
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = '';
    
    users.forEach(u => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span class="font-mono" style="font-weight: 600; color: #f8fafc;">${u.username}</span></td>
            <td>${u.full_name}</td>
            <td style="color: #94a3b8;">${u.email}</td>
            <td><span class="badge badge-role">${u.role}</span></td>
            <td><span class="badge badge-valid">${u.status}</span></td>
            <td>
                ${u.user_id !== currentUser.user_id ? 
                    `<button class="btn-danger" onclick="deleteUserAccount(${u.user_id}, '${u.username}')">Revoke</button>` 
                    : '<span style="color: #64748b; font-size: 0.78rem;">(Active)</span>'}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteUserAccount(userId, username) {
    if (!confirm(`Confirm revocation of operator account '${username}'?`)) return;
    
    const res = await fetch(`/api/users/${userId}`, { method: 'DELETE' });
    if (res.ok) {
        showToast('success', `Account '${username}' revoked.`);
        loadUsers();
    } else {
        const err = await res.json();
        showToast('error', err.detail || 'Operation failed.');
    }
}

// --- Load Security Audit Logs ---
async function loadAuditLogs() {
    const res = await fetch('/api/audit?limit=100');
    if (!res.ok) return;
    const logs = await res.json();
    
    const tbody = document.getElementById('audit-table-body');
    tbody.innerHTML = '';
    
    if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #64748b; padding: 24px;">No security events recorded.</td></tr>`;
        return;
    }
    
    logs.forEach(l => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="font-mono" style="color: #64748b;">#${l.log_id}</td>
            <td><code class="font-mono" style="color: #60a5fa; font-size: 0.8rem;">${l.action}</code></td>
            <td><span class="badge badge-role">${l.module}</span></td>
            <td style="color: #cbd5e1; font-size: 0.84rem;">${l.description || '—'}</td>
            <td style="color: #64748b; font-size: 0.8rem;" class="font-mono">${new Date(l.created_at).toLocaleString()}</td>
            <td><strong style="color: #f8fafc; font-size: 0.85rem;">${l.performed_by}</strong></td>
        `;
        tbody.appendChild(tr);
    });
}
