import streamlit as st
import auth
import db
import email_utils
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
            st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Secure Authentication</h3>", unsafe_allow_html=True)
            
            login_method = st.radio("Select Login Method", ["Password", "Gmail OTP"], horizontal=True, key="login_method_selector")
            
            if login_method == "Password":
                with st.container(border=True):
                    username = st.text_input("Username", key="login_username_field", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", key="login_password_field", placeholder="Enter your password")
                    
                    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
                    login_btn = st.button("Log In", key="login_submit_btn")
                    

                    
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
            else: # Gmail OTP
                with st.container(border=True):
                    email = st.text_input("Gmail Address", key="login_email_field", placeholder="Enter your registered email")
                    
                    # Store sent OTP state
                    if "otp" not in st.session_state:
                        st.session_state.otp = None
                    if "otp_sent_email" not in st.session_state:
                        st.session_state.otp_sent_email = None
                        
                    send_otp_btn = st.button("Send OTP Verification", key="send_otp_btn")
                    
                    if send_otp_btn:
                        if not email:
                            st.warning("Please enter your Gmail address.")
                        else:
                            # Verify if email exists
                            check_q = "SELECT user_id FROM users WHERE email = %s"
                            try:
                                res = db.execute_query(check_q, (email,), fetch=True)
                                if not res:
                                    st.error("This email is not registered. Please create an account first.")
                                else:
                                    # Generate and send OTP
                                    otp = email_utils.generate_otp()
                                    st.session_state.otp = otp
                                    st.session_state.otp_sent_email = email
                                    
                                    try:
                                        email_utils.send_otp_email(email, otp)
                                        st.success(f"OTP has been successfully sent to {email}!")
                                    except Exception as e:
                                        st.warning(f"⚠️ [Dev Mode] SMTP failed to send: {e}. OTP printed below.")
                                        st.info(f"🔑 Mock Console OTP: **{otp}**")
                            except Exception as db_err:
                                st.error(f"Database query error: {db_err}")
                                
                    if st.session_state.otp and st.session_state.otp_sent_email == email:
                        st.markdown("---")
                        otp_input = st.text_input("Enter 6-Digit OTP", key="otp_input_field", placeholder="e.g. 123456")
                        verify_otp_btn = st.button("Verify & Log In", key="verify_otp_btn")
                        
                        if verify_otp_btn:
                            if not otp_input:
                                st.warning("Please enter the verification code.")
                            elif otp_input.strip() == st.session_state.otp:
                                success, message = auth.login_via_email(email)
                                if success:
                                    st.success(message)
                                    # Clear OTP states
                                    st.session_state.otp = None
                                    st.session_state.otp_sent_email = None
                                    st.rerun()
                                else:
                                    st.error(message)
                            else:
                                st.error("Invalid verification code. Please try again.")
                        
        with tab_register:
            if "reg_step" not in st.session_state:
                st.session_state.reg_step = "form"
                st.session_state.reg_data = {}
                st.session_state.reg_otp = None
                
            if st.session_state.reg_step == "form":
                with st.container(border=True):
                    st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Create Account</h3>", unsafe_allow_html=True)
                    
                    reg_name = st.text_input("Full Name", key="reg_name_field", placeholder="e.g. John Doe")
                    reg_username = st.text_input("Username", key="reg_username_field", placeholder="Choose a username")
                    reg_email = st.text_input("Email Address", key="reg_email_field", placeholder="e.g. john@example.com")
                    reg_phone = st.text_input("Phone Number", key="reg_phone_field", placeholder="e.g. +919999999999 (Required for SMS OTP)")
                    reg_password = st.text_input("Password", type="password", key="reg_pw_field", placeholder="Create a secure password")
                    reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm_field", placeholder="Re-enter password")
                    
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    reg_verify_method = st.radio("Send Verification Code via", ["Email", "SMS (Twilio)"], horizontal=True, key="reg_verify_method_radio")
                    
                    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
                    register_btn = st.button("Send Verification Code", key="reg_submit_btn")
                    
                if register_btn:
                    if not all([reg_name, reg_username, reg_email, reg_password, reg_confirm]):
                        st.warning("All fields except Phone Number are required.")
                    elif reg_password != reg_confirm:
                        st.error("Passwords do not match. Please verify and try again.")
                    elif reg_verify_method == "SMS (Twilio)" and not reg_phone:
                        st.warning("Phone Number is required to send an SMS verification code.")
                    else:
                        # Check if username or email exists
                        check_q = "SELECT user_id FROM users WHERE username = %s OR email = %s"
                        try:
                            existing = db.execute_query(check_q, (reg_username, reg_email), fetch=True)
                            if existing:
                                st.error("Username or Email is already registered.")
                            else:
                                # Generate OTP and switch step
                                otp = email_utils.generate_otp()
                                st.session_state.reg_otp = otp
                                st.session_state.reg_method = reg_verify_method
                                st.session_state.reg_data = {
                                    'name': reg_name,
                                    'username': reg_username,
                                    'email': reg_email,
                                    'phone': reg_phone,
                                    'password': reg_password
                                }
                                
                                try:
                                    if reg_verify_method == "SMS (Twilio)":
                                        email_utils.send_sms_otp(reg_phone, otp)
                                        st.success(f"Verification code sent to {reg_phone} via SMS!")
                                    else:
                                        email_utils.send_otp_email(reg_email, otp)
                                        st.success(f"Verification code sent to {reg_email}!")
                                except Exception as e:
                                    method_str = "SMS" if reg_verify_method == "SMS (Twilio)" else "SMTP"
                                    st.warning(f"⚠️ [Dev Mode] {method_str} failed to send: {e}. OTP printed below.")
                                    st.info(f"🔑 Mock Console OTP: **{otp}**")
                                
                                import time
                                time.sleep(1.0)
                                st.session_state.reg_step = "verify"
                                st.rerun()
                        except Exception as e:
                            st.error(f"Registration failed: {e}")
                            
            elif st.session_state.reg_step == "verify":
                with st.container(border=True):
                    st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Verify Email Address</h3>", unsafe_allow_html=True)
                    st.info(f"An OTP was sent to **{st.session_state.reg_data.get('email', '')}**")
                    
                    reg_otp_input = st.text_input("Enter 6-Digit Verification Code", key="reg_otp_input")
                    
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    colA, colB = st.columns(2)
                    with colA:
                        verify_btn = st.button("Verify & Create Account")
                    with colB:
                        cancel_btn = st.button("Cancel & Go Back")
                        
                if cancel_btn:
                    st.session_state.reg_step = "form"
                    st.session_state.reg_otp = None
                    st.rerun()
                    
                if verify_btn:
                    if not reg_otp_input:
                        st.warning("Please enter the verification code.")
                    elif reg_otp_input.strip() == st.session_state.reg_otp:
                        # Success, insert to DB
                        data = st.session_state.reg_data
                        hashed_pw = auth.hash_password(data['password'])
                        insert_q = """
                            INSERT INTO users (full_name, username, email, phone, password_hash, role, status)
                            VALUES (%s, %s, %s, %s, %s, 'Guest', 'Active')
                        """
                        try:
                            new_user_id = db.execute_query(insert_q, (data['name'], data['username'], data['email'], data['phone'], hashed_pw), commit=True)
                            auth.log_audit(new_user_id, "REGISTER_USER", "Authentication", f"User verified and registered: {data['username']} (Role: Guest)")
                            
                            # Success, clear reg states
                            st.session_state.reg_step = "form"
                            st.session_state.reg_data = {}
                            st.session_state.reg_otp = None
                            
                            st.success("🎉 Account created successfully! Redirecting to login...")
                            import time
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Database insertion failed: {e}")
                    else:
                        st.error("Invalid verification code. Please try again.")

if __name__ == "__main__":
    show_login()
