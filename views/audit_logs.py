import streamlit as st
import db
import pandas as pd
from styling import apply_custom_css

def show_audit_logs():
    apply_custom_css()
    
    st.markdown('<h2 style="margin-top:0;">🛡️ System Audit Logs</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Review system security events, modifications, and user logins.</p>", unsafe_allow_html=True)
    
    # Filters
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0; margin-bottom:15px;'>Logs Filtering</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            keyword = st.text_input("Search Description", placeholder="e.g. admin...", key="audit_desc_search")
        with col2:
            module_filter = st.selectbox("Module", ["All", "Authentication", "Validation", "UserManagement", "Settings"], key="audit_mod_filter")
        with col3:
            action_filter = st.text_input("Action", placeholder="e.g. LOGIN_SUCCESS", key="audit_action_filter")
            
    # DB read query
    query = """
        SELECT a.log_id, u.username as 'User', a.module as 'Module', 
               a.action as 'Action', a.description as 'Event Details', a.created_at as 'Timestamp'
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.user_id
        WHERE 1=1
    """
    params = []
    
    if keyword:
        query += " AND a.description LIKE %s"
        params.append(f"%{keyword.strip()}%")
        
    if module_filter != "All":
        query += " AND a.module = %s"
        params.append(module_filter)
        
    if action_filter:
        query += " AND a.action LIKE %s"
        params.append(f"%{action_filter.strip().upper()}%")
        
    query += " ORDER BY a.created_at DESC"
    
    try:
        logs = db.execute_query(query, tuple(params), fetch=True)
        if logs:
            df = pd.DataFrame(logs)
            
            # Action Row
            col_stat, col_btn = st.columns([3, 1])
            with col_stat:
                st.markdown(f"<p style='color: #64748b; margin-top: 10px;'>Showing {len(df)} audit logs matching filters</p>", unsafe_allow_html=True)
            with col_btn:
                # Export to CSV
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv_data,
                    file_name="kyc_audit_logs.csv",
                    mime="text/csv",
                    key="export_audit_csv_btn"
                )
                
            # Table View
            display_df = df.drop(columns=['log_id'])
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No matching audit logs found.")
    except Exception as e:
        st.error(f"Error fetching system audit logs: {e}")

if __name__ == "__main__":
    show_audit_logs()
