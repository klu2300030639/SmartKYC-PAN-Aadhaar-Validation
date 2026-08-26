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

# Defining Page Callables with Native Vector Material Symbols
login_page = st.Page(show_login, title="Authentication", icon=":material/lock:")
dashboard_page = st.Page(show_dashboard, title="Overview", icon=":material/dashboard:")
validate_page = st.Page(show_validate, title="Verify Documents", icon=":material/verified_user:")
history_page = st.Page(show_history, title="Audit Registry", icon=":material/history:")
users_page = st.Page(show_users, title="User Directory", icon=":material/manage_accounts:")
audit_page = st.Page(show_audit_logs, title="Security Logs", icon=":material/shield:")
settings_page = st.Page(show_settings, title="Configuration", icon=":material/settings:")

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
    else: # Guest role
        nav_pages = [dashboard_page, validate_page]
    
    # Sidebar Header Details
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0px 16px 0px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="display: flex; align-items: center; gap: 8px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
                <span style="margin: 0; color: #ffffff; font-size: 1.25rem; font-weight: 700;">SmartKYC</span>
            </div>
            <div style="margin-top: 8px; font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Active Account</div>
            <div style="font-size: 0.88rem; color: #f8fafc; font-weight: 600; margin-top: 2px;">{st.session_state.get('full_name')}</div>
            <span class="badge badge-role" style="margin-top: 4px; display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; background: rgba(59, 130, 246, 0.12); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3);">{st.session_state.get('role')}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
        
    pg = st.navigation(nav_pages)
    
    # Sidebar Footer (Logout Button)
    with st.sidebar:
        st.markdown("<div style='position: fixed; bottom: 20px; width: 220px;'>", unsafe_allow_html=True)
        if st.button("Sign Out", key="sidebar_logout_btn"):
            handle_logout()
        st.markdown("</div>", unsafe_allow_html=True)


# Inject Global Styling Custom CSS and Execute Page
apply_custom_css()
pg.run()
