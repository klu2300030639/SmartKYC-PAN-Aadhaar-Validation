import streamlit as st
import auth
from styling import apply_custom_css

def show_login():
    apply_custom_css()
    
    # Title Banner with vibrant design
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <h1 style="font-size: 3.2rem; margin-bottom: 0;">
            <span class="brand-text">SmartKYC</span>
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">
            PAN & Aadhaar Identity Verification System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card Container
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        tab_login, tab_register = st.tabs(["🔒 Sign In", "📝 Create Account"])
        
        with tab_login:
            with st.container(border=True):
                st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Secure Authentication</h3>", unsafe_allow_html=True)
                
                username = st.text_input("Username", key="login_username_field", placeholder="Enter your username")
                password = st.text_input("Password", type="password", key="login_password_field", placeholder="Enter your password")
                
                st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
                login_btn = st.button("Log In", key="login_submit_btn")
                
                # Admin Hint
                st.markdown("""
                <div style="text-align: center; margin-top: 20px; font-size: 0.85rem; color: #94a3b8;">
                    💡 Admin Hint: Username: <b>admin</b> | Password: <b>admin123</b>
                </div>
                """, unsafe_allow_html=True)
                
            if login_btn:
                if not username or not password:
                    st.warning("Please fill in both username and password.")
                else:
                    success, message = auth.login(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                        
        with tab_register:
            with st.container(border=True):
                st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Create Account</h3>", unsafe_allow_html=True)
                
                reg_name = st.text_input("Full Name", key="reg_name_field", placeholder="e.g. John Doe")
                reg_username = st.text_input("Username", key="reg_username_field", placeholder="Choose a username")
                reg_email = st.text_input("Email Address", key="reg_email_field", placeholder="e.g. john@example.com")
                reg_phone = st.text_input("Phone Number (Optional)", key="reg_phone_field", placeholder="e.g. +919999999999")
                reg_password = st.text_input("Password", type="password", key="reg_pw_field", placeholder="Create a secure password")
                reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm_field", placeholder="Re-enter password")
                
                st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
                register_btn = st.button("Register Account", key="reg_submit_btn")
                
            if register_btn:
                if not all([reg_name, reg_username, reg_email, reg_password, reg_confirm]):
                    st.warning("All fields except Phone Number are required.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match. Please verify and try again.")
                else:
                    # Check if username or email exists
                    check_q = "SELECT user_id FROM users WHERE username = %s OR email = %s"
                    try:
                        existing = db.execute_query(check_q, (reg_username, reg_email), fetch=True)
                        if existing:
                            st.error("Username or Email is already registered.")
                        else:
                            # Create limited user ('Guest')
                            hashed_pw = auth.hash_password(reg_password)
                            insert_q = """
                                INSERT INTO users (full_name, username, email, phone, password_hash, role, status)
                                VALUES (%s, %s, %s, %s, %s, 'Guest', 'Active')
                            """
                            new_user_id = db.execute_query(insert_q, (reg_name, reg_username, reg_email, reg_phone, hashed_pw), commit=True)
                            auth.log_audit(new_user_id, "REGISTER_USER", "Authentication", f"User self-registered: {reg_username} (Role: Guest)")
                            st.success("Account created successfully! Please switch to the 'Sign In' tab to log in.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

if __name__ == "__main__":
    show_login()
