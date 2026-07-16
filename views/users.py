import streamlit as st
import db
import auth
import pandas as pd
from styling import apply_custom_css

def show_users():
    apply_custom_css()
    
    # Secure access check
    if st.session_state.get('role') != 'Admin':
        st.error("Access Denied: You do not have permissions to view this page.")
        return
        
    st.markdown('<h2 style="margin-top:0;">👥 User Administration</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Create, configure, and manage user accounts and application roles.</p>", unsafe_allow_html=True)
    
    tab_list, tab_create, tab_edit = st.tabs(["📋 Directory", "➕ Add User", "✏️ Modify User"])
    
    with tab_list:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0;'>System Accounts</h4>", unsafe_allow_html=True)
            
            query = "SELECT user_id, full_name, username, email, phone, role, status, created_at FROM users"
            try:
                users_list = db.execute_query(query, fetch=True)
                if users_list:
                    df = pd.DataFrame(users_list)
                    df.columns = ['ID', 'Full Name', 'Username', 'Email', 'Phone', 'Role', 'Status', 'Joined Date']
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No user accounts registered.")
            except Exception as e:
                st.error(f"Error loading users directory: {e}")
        
    with tab_create:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top: 0;'>Register a New User</h4>", unsafe_allow_html=True)
            
            with st.form("create_user_form", clear_on_submit=True):
                full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
                new_username = st.text_input("Username", placeholder="e.g. johndoe")
                email = st.text_input("Email Address", placeholder="e.g. john@smartkyc.com")
                phone = st.text_input("Phone Number", placeholder="e.g. +919999999999")
                password = st.text_input("Password", type="password", placeholder="Enter secure password")
                role = st.selectbox("Role Permission", ["Guest", "User", "Admin"])
                status = st.selectbox("Status", ["Active", "Suspended"])
                
                submit_btn = st.form_submit_button("Add User Account")
                
                if submit_btn:
                    if not all([full_name, new_username, email, password]):
                        st.warning("Full Name, Username, Email, and Password are required fields.")
                    else:
                        # Check if username or email already exists
                        check_q = "SELECT user_id FROM users WHERE username = %s OR email = %s"
                        existing = db.execute_query(check_q, (new_username, email), fetch=True)
                        if existing:
                            st.error("Error: Username or Email is already registered.")
                        else:
                            # Hash password
                            hashed_pw = auth.hash_password(password)
                            insert_q = """
                                INSERT INTO users (full_name, username, email, phone, password_hash, role, status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """
                            try:
                                new_id = db.execute_query(insert_q, (full_name, new_username, email, phone, hashed_pw, role, status), commit=True)
                                auth.log_audit(st.session_state.get('user_id'), "CREATE_USER", "UserManagement", f"Created user {new_username} (ID: {new_id}, Role: {role})")
                                st.success(f"Successfully registered user: {new_username}")
                            except Exception as e:
                                st.error(f"Database write failed: {e}")
        
    with tab_edit:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0;'>Update Account Status/Role</h4>", unsafe_allow_html=True)
            
            # Load user names for selectbox
            try:
                users_res = db.execute_query("SELECT username FROM users", fetch=True)
                usernames = [u['username'] for u in users_res] if users_res else []
            except Exception:
                usernames = []
                
            if usernames:
                selected_username = st.selectbox("Select Account", usernames, key="select_user_to_modify")
                
                # Fetch current details of selected user
                current_details_q = "SELECT role, status, full_name FROM users WHERE username = %s"
                current_details = db.execute_query(current_details_q, (selected_username,), fetch=True)
                
                if current_details:
                    curr_role = current_details[0]['role']
                    curr_status = current_details[0]['status']
                    curr_name = current_details[0]['full_name']
                    
                    st.markdown(f"Currently managing: **{curr_name}** (`{selected_username}`)")
                    
                    with st.form("modify_user_form"):
                        new_role = st.selectbox("New Role Permission", ["Guest", "User", "Admin"], index=["Guest", "User", "Admin"].index(curr_role))
                        new_status = st.selectbox("New Status", ["Active", "Suspended"], index=["Active", "Suspended"].index(curr_status))
                        
                        update_btn = st.form_submit_button("Update Account Settings")
                        
                        if update_btn:
                            update_q = "UPDATE users SET role = %s, status = %s WHERE username = %s"
                            try:
                                db.execute_query(update_q, (new_role, new_status, selected_username), commit=True)
                                auth.log_audit(st.session_state.get('user_id'), "UPDATE_USER", "UserManagement", 
                                               f"Updated user {selected_username} (Role: {curr_role}->{new_role}, Status: {curr_status}->{new_status})")
                                st.success(f"Successfully updated account settings for {selected_username}")
                            except Exception as e:
                                st.error(f"Update query failed: {e}")
                                
                    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                    with st.expander("Danger Zone ⚠️"):
                        st.warning(f"Are you sure you want to completely delete the account for **{selected_username}**? This action cannot be undone.")
                        delete_btn = st.button("Delete User Account", type="primary", key="del_user_btn")
                        if delete_btn:
                            if selected_username == st.session_state.get("username"):
                                st.error("You cannot delete your own active Admin account!")
                            else:
                                del_q = "DELETE FROM users WHERE username = %s"
                                try:
                                    db.execute_query(del_q, (selected_username,), commit=True)
                                    auth.log_audit(st.session_state.get('user_id'), "DELETE_USER", "UserManagement", f"Deleted user account: {selected_username}")
                                    st.success(f"Successfully deleted account: {selected_username}")
                                    import time
                                    time.sleep(1)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to delete user: {e}")
            else:
                st.info("No active accounts found.")

if __name__ == "__main__":
    show_users()
