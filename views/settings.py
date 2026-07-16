import streamlit as st
import db
import auth
from styling import apply_custom_css

def show_settings():
    apply_custom_css()
    
    st.markdown('<h2 style="margin-top:0;">⚙️ Application Configuration</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Manage visual interface parameters, database connectivity, and maintenance operations.</p>", unsafe_allow_html=True)
    
    # Card 1: Theme Selection
    st.markdown('<div class="kyc-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0;'>Interface Appearance</h4>", unsafe_allow_html=True)
    
    # Read current theme from DB
    current_theme = "dark"
    try:
        theme_res = db.execute_query("SELECT setting_value FROM application_settings WHERE setting_key = 'theme'", fetch=True)
        if theme_res:
            current_theme = theme_res[0]['setting_value'].lower()
    except Exception:
        pass
        
    theme_options = ["dark", "light"]
    selected_theme = st.radio("Choose App Theme", theme_options, index=theme_options.index(current_theme), horizontal=True, key="settings_theme_radio")
    
    apply_theme_btn = st.button("Apply Appearance Settings", key="settings_apply_theme_btn")
    if apply_theme_btn:
        try:
            db.execute_query("UPDATE application_settings SET setting_value = %s WHERE setting_key = 'theme'", (selected_theme,), commit=True)
            st.session_state.theme = selected_theme
            auth.log_audit(st.session_state.get('user_id'), "UPDATE_SETTINGS", "Settings", f"Changed UI theme to {selected_theme}")
            st.success(f"Theme successfully updated to {selected_theme.upper()}! Refreshing...")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to update theme in database: {e}")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 2: Database Configuration details (read-only info)
    st.markdown('<div class="kyc-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0;'>Database Connectivity Test</h4>", unsafe_allow_html=True)
    
    config = db.get_connection_config()
    st.text(f"Database Server: {config['host']}")
    st.text(f"Port: {config['port']}")
    st.text(f"Schema Name: {config['database']}")
    st.text(f"User: {config['user']}")
    
    test_conn_btn = st.button("🔌 Test Connection", key="settings_test_db_btn")
    if test_conn_btn:
        ok = db.check_db_connection()
        if ok:
            st.markdown("<p style='color: #10b981; font-weight: bold;'>● Database Connection Successful!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #ef4444; font-weight: bold;'>● Database Connection Failed!</p>", unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 3: Admin Maintenance Options (Purge operations)
    if st.session_state.get('role') == 'Admin':
        st.markdown('<div class="kyc-card" style="border-left: 5px solid #ef4444 !important;">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; color:#ef4444;'>🛡️ Administrative Maintenance Operations</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.9rem; color:#94a3b8;'>Warning: These actions are destructive and cannot be undone.</p>", unsafe_allow_html=True)
        
        col_purge_h, col_purge_l = st.columns(2)
        
        with col_purge_h:
            purge_history = st.button("🗑 Purge KYC History", key="settings_purge_history_btn")
            if purge_history:
                try:
                    db.execute_query("DELETE FROM validation_history", commit=True)
                    auth.log_audit(st.session_state.get('user_id'), "PURGE_HISTORY", "Settings", "Purged all KYC validation records from database")
                    st.success("Successfully deleted all verification history!")
                except Exception as e:
                    st.error(f"Purge failed: {e}")
                    
        with col_purge_l:
            purge_logs = st.button("🗑 Purge Audit Logs", key="settings_purge_logs_btn")
            if purge_logs:
                try:
                    # Clear audit logs (except this action itself)
                    db.execute_query("DELETE FROM audit_logs", commit=True)
                    auth.log_audit(st.session_state.get('user_id'), "PURGE_AUDIT_LOGS", "Settings", "Purged all system audit logs")
                    st.success("Successfully purged system audit logs!")
                except Exception as e:
                    st.error(f"Purge failed: {e}")
                    
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_settings()
