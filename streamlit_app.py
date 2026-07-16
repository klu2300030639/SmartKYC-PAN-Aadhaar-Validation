import streamlit as st
import db
import auth
from views.login import show_login
from views.dashboard import show_dashboard
from views.validate import show_validate
from views.history import show_history
from views.audit_logs import show_audit_logs
from views.users import show_users
from views.settings import show_settings
from styling import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartKYC Validator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Dynamic Page Navigation API (Streamlit >= 1.35.0)
def handle_logout():
    auth.logout()
    st.success("Logged out successfully!")
    st.rerun()

# Defining Page Callables
login_page = st.Page(show_login, title="Login", icon="🔒")
dashboard_page = st.Page(show_dashboard, title="Dashboard", icon="📊")
validate_page = st.Page(show_validate, title="Verify KYC", icon="🔍")
history_page = st.Page(show_history, title="KYC History", icon="⏳")
audit_page = st.Page(show_audit_logs, title="Audit Logs", icon="🛡️")
users_page = st.Page(show_users, title="User Directory", icon="👥")
settings_page = st.Page(show_settings, title="Configuration", icon="⚙️")

# Navigation Setup
if not st.session_state.logged_in:
    # Force login page only
    pg = st.navigation([login_page], position="hidden")
else:
    # Add pages dynamically based on permissions
    role = st.session_state.get('role')
    if role == 'Admin':
        nav_pages = [dashboard_page, validate_page, history_page, users_page, audit_page, settings_page]
    elif role == 'User':
        nav_pages = [dashboard_page, validate_page, settings_page]
    else: # Guest role (self-registered limited access)
        nav_pages = [dashboard_page, validate_page]
    
    # Sidebar Header Details
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0px 20px 0px; border-bottom: 1px solid #334155;">
            <h2 style="margin: 0; color: #3b82f6; font-size: 1.8rem;">SmartKYC</h2>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #94a3b8;">
                👤 User: <b>{st.session_state.get('full_name')}</b> ({st.session_state.get('role')})
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
    pg = st.navigation(nav_pages)
    
    # Sidebar Footer (Logout Button)
    with st.sidebar:
        st.markdown("<div style='position: fixed; bottom: 20px; width: 220px;'>", unsafe_allow_html=True)
        if st.button("🚪 Log Out", key="sidebar_logout_btn"):
            handle_logout()
        st.markdown("</div>", unsafe_allow_html=True)

# Inject Global Styling Custom CSS and Execute Page
apply_custom_css()
pg.run()
