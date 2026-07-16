import streamlit as st
import db
import pandas as pd
import plotly.express as px
from styling import apply_custom_css, kpi_card

def show_dashboard():
    apply_custom_css()
    
    st.markdown('<h2 style="margin-top:0;">📊 Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Real-time analytics and validation insights</p>", unsafe_allow_html=True)
      # Scope queries based on user role (Guests only see their own activity)
    role = st.session_state.get('role')
    user_id = st.session_state.get('user_id')
    
    if role == 'Guest':
        where_clause = " WHERE user_id = %s"
        valid_where = " WHERE status = 'Valid' AND user_id = %s"
        invalid_where = " WHERE status = 'Invalid' AND user_id = %s"
        query_params = (user_id,)
    else:
        where_clause = ""
        valid_where = " WHERE status = 'Valid'"
        invalid_where = " WHERE status = 'Invalid'"
        query_params = ()
        
    total_query = f"SELECT COUNT(*) as count FROM validation_history{where_clause}"
    valid_query = f"SELECT COUNT(*) as count FROM validation_history{valid_where}"
    invalid_query = f"SELECT COUNT(*) as count FROM validation_history{invalid_where}"
    
    try:
        total_res = db.execute_query(total_query, query_params, fetch=True)
        valid_res = db.execute_query(valid_query, query_params, fetch=True)
        invalid_res = db.execute_query(invalid_query, query_params, fetch=True)
        
        total_count = total_res[0]['count'] if total_res else 0
        valid_count = valid_res[0]['count'] if valid_res else 0
        invalid_count = invalid_res[0]['count'] if invalid_res else 0
        success_rate = round((valid_count / total_count * 100), 1) if total_count > 0 else 100.0
    except Exception as e:
        st.error(f"Error fetching dashboard metrics: {e}")
        total_count = valid_count = invalid_count = 0
        success_rate = 0.0

    # Metrics row using styled HTML templates
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Verifications", f"{total_count:,}", "📋")
    with col2:
        kpi_card("Valid Records", f"{valid_count:,}", "✅")
    with col3:
        kpi_card("Invalid Records", f"{invalid_count:,}", "❌")
    with col4:
        kpi_card("Verification Success", f"{success_rate}%", "🛡️")
        
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    # Graphs Row
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0;'>Document Distribution</h4>", unsafe_allow_html=True)
            
            if role == 'Guest':
                doc_query = "SELECT document_type, COUNT(*) as count FROM validation_history WHERE user_id = %s GROUP BY document_type"
                doc_params = (user_id,)
            else:
                doc_query = "SELECT document_type, COUNT(*) as count FROM validation_history GROUP BY document_type"
                doc_params = ()
                
            try:
                doc_data = db.execute_query(doc_query, doc_params, fetch=True)
                if doc_data:
                    df_doc = pd.DataFrame(doc_data)
                    fig_doc = px.pie(df_doc, values='count', names='document_type', 
                                     hole=0.4,
                                     color_discrete_sequence=['#3b82f6', '#10b981'])
                    fig_doc.update_layout(margin=dict(t=0, b=0, l=0, r=0), 
                                          height=220, 
                                          paper_bgcolor='rgba(0,0,0,0)', 
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          font_color='#94a3b8' if st.session_state.get('theme') == 'dark' else '#0f172a')
                    st.plotly_chart(fig_doc, use_container_width=True)
                else:
                    st.info("No verification history available to visualize.")
            except Exception as e:
                st.error(f"Error drawing pie chart: {e}")
        
    with col_right:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0;'>Status Breakdown</h4>", unsafe_allow_html=True)
            
            if role == 'Guest':
                status_query = "SELECT status, COUNT(*) as count FROM validation_history WHERE user_id = %s GROUP BY status"
                status_params = (user_id,)
            else:
                status_query = "SELECT status, COUNT(*) as count FROM validation_history GROUP BY status"
                status_params = ()
                
            try:
                status_data = db.execute_query(status_query, status_params, fetch=True)
                if status_data:
                    df_status = pd.DataFrame(status_data)
                    fig_status = px.bar(df_status, x='status', y='count', 
                                        color='status',
                                        color_discrete_map={'Valid': '#10b981', 'Invalid': '#ef4444'})
                    fig_status.update_layout(margin=dict(t=10, b=10, l=10, r=10), 
                                             height=220,
                                             paper_bgcolor='rgba(0,0,0,0)', 
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             xaxis_title=None, yaxis_title="Count",
                                             font_color='#94a3b8' if st.session_state.get('theme') == 'dark' else '#0f172a')
                    st.plotly_chart(fig_status, use_container_width=True)
                else:
                    st.info("No verification history available to visualize.")
            except Exception as e:
                st.error(f"Error drawing bar chart: {e}")
 
    # Recent Activity Row
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0;'>Recent Activity</h4>", unsafe_allow_html=True)
        
        if role == 'Guest':
            recent_query = """
                SELECT v.document_type, v.document_number, v.status, v.reason, v.validated_at, u.username
                FROM validation_history v
                LEFT JOIN users u ON v.user_id = u.user_id
                WHERE v.user_id = %s
                ORDER BY v.validated_at DESC
                LIMIT 5
            """
            recent_params = (user_id,)
        else:
            recent_query = """
                SELECT v.document_type, v.document_number, v.status, v.reason, v.validated_at, u.username
                FROM validation_history v
                LEFT JOIN users u ON v.user_id = u.user_id
                ORDER BY v.validated_at DESC
                LIMIT 5
            """
            recent_params = ()
            
        try:
            recent_data = db.execute_query(recent_query, recent_params, fetch=True)
            if recent_data:
                df_recent = pd.DataFrame(recent_data)
                # Rename columns for presentation
                df_recent.columns = ['Doc Type', 'Doc Number', 'Status', 'Message/Reason', 'Timestamp', 'Verified By']
                # Reorder
                st.dataframe(df_recent, use_container_width=True, hide_index=True)
            else:
                st.info("No recent verification records.")
        except Exception as e:
            st.error(f"Error fetching recent activity: {e}")activity: {e}")

if __name__ == "__main__":
    show_dashboard()
