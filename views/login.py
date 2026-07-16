import streamlit as st
import db
import auth
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
