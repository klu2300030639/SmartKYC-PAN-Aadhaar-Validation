import streamlit as st
import db
import auth
import email_utils
from styling import apply_custom_css

def show_login():
    apply_custom_css()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #3b82f6; font-size: 3rem; margin-bottom: 0;">
            SmartKYC
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">
            PAN & Aadhaar Identity Verification System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card Container
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Secure Authentication</h3>", unsafe_allow_html=True)
        
        login_method = st.radio("Select Login Method", ["Password", "Gmail OTP"], horizontal=True, key="login_method_selector")
        
        if login_method == "Password":
            with st.form("password_login_form", border=True):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                login_btn = st.form_submit_button("Log In")
                
            if login_btn:
                if not username or not password:
                    st.warning("Please fill in both username and password.")
                else:
                    success, message = auth.login(username, password)
                    if success:
                        st.success(message)
                        import time
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(message)
        else: # Gmail OTP
            with st.container(border=True):
                # Form 1: Email Input
                with st.form("otp_email_form"):
                    email = st.text_input("Gmail Address", key="login_email_field", placeholder="Enter your registered email")
                    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                    send_otp_btn = st.form_submit_button("Send OTP Verification")
                
                # Store sent OTP state
                if "otp" not in st.session_state:
                    st.session_state.otp = None
                if "otp_sent_email" not in st.session_state:
                    st.session_state.otp_sent_email = None
                    
                if send_otp_btn:
                    if not email:
                        st.warning("Please enter your Gmail address.")
                    else:
                        # Verify if email exists
                        check_q = "SELECT user_id FROM users WHERE email = %s"
                        try:
                            res = db.execute_query(check_q, (email,), fetch=True)
                            if not res:
                                st.error("This email is not registered. Please contact an administrator to create an account.")
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
                    # Form 2: OTP Input
                    with st.form("otp_verify_form"):
                        otp_input = st.text_input("Enter 6-Digit OTP", key="otp_input_field", placeholder="e.g. 123456")
                        st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                        verify_otp_btn = st.form_submit_button("Verify & Log In")
                    
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
                                import time
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Invalid verification code. Please try again.")

if __name__ == "__main__":
    show_login()
