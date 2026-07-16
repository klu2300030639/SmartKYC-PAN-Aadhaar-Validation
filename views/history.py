import streamlit as st
import db
import pandas as pd
from styling import apply_custom_css

def show_history():
    apply_custom_css()
    
    st.markdown('<h2 style="margin-top:0;">⏳ Verification History</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>View, filter, and export past verification transactions.</p>", unsafe_allow_html=True)
    
    # Filter tools in a card
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0; margin-bottom:15px;'>Search Filters</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("Document Number", placeholder="Search by number...", key="history_search_q")
        with col2:
            doc_type_filter = st.selectbox("Document Type", ["All", "PAN", "Aadhaar"], key="history_doc_filter")
        with col3:
            status_filter = st.selectbox("Status", ["All", "Valid", "Invalid"], key="history_status_filter")
    
    # Construct SQL query dynamically based on filters
    query = """
        SELECT v.validation_id, u.username as 'Verified By', v.document_type as 'Doc Type', 
               v.document_number as 'Doc Number', v.status as 'Status', 
               v.reason as 'Reason / Message', v.validated_at as 'Timestamp'
        FROM validation_history v
        LEFT JOIN users u ON v.user_id = u.user_id
        WHERE 1=1
    """
    params = []
    
    if search_query:
        query += " AND v.document_number LIKE %s"
        params.append(f"%{search_query.strip().upper()}%")
        
    if doc_type_filter != "All":
        query += " AND v.document_type = %s"
        params.append(doc_type_filter)
        
    if status_filter != "All":
        query += " AND v.status = %s"
        params.append(status_filter)
        
    query += " ORDER BY v.validated_at DESC"
    
    try:
        records = db.execute_query(query, tuple(params), fetch=True)
        if records:
            df = pd.DataFrame(records)
            
            # Action Row
            col_stat, col_btn = st.columns([3, 1])
            with col_stat:
                st.markdown(f"<p style='color: #64748b; margin-top: 10px;'>Showing {len(df)} records matching filters</p>", unsafe_allow_html=True)
            with col_btn:
                # Export to CSV
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv_data,
                    file_name="kyc_verification_history.csv",
                    mime="text/csv",
                    key="export_csv_btn"
                )
            
            # Display Table
            # Remove validation_id from display but keep it in df
            display_df = df.drop(columns=['validation_id'])
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No matching records found in verification history.")
    except Exception as e:
        st.error(f"Error reading verification history: {e}")

if __name__ == "__main__":
    show_history()
