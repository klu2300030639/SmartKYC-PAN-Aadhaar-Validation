import streamlit as st
import db
import auth
from styling import apply_custom_css

def show_login():
    apply_custom_css()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <div style="display: inline-block; margin-bottom: 15px;">
            <svg width="70" height="70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.6));">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" fill="url(#blue-grad)" />
                <path d="M7.5 12L10.5 15L16.5 9" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="blue-grad" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#60A5FA"/>
                        <stop offset="1" stop-color="#2563EB"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <h1 style="color: #3b82f6; font-size: 2.8rem; margin-bottom: 0; line-height: 1;">
            SmartKYC
        </h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top: 8px;">
            PAN & Aadhaar Identity Verification System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card Container
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Secure Authentication</h3>", unsafe_allow_html=True)
        
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

if __name__ == "__main__":
    show_login()
