import streamlit as st
import db
import auth
from styling import apply_custom_css

def show_login():
    apply_custom_css()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="display: inline-block; margin-bottom: 12px;">
            <svg width="68" height="68" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 2px 8px rgba(37, 99, 235, 0.4));">
                <path d="M12 2.5C12 2.5 5 5 5 6.5V11.5C5 16 12 19.5 12 19.5C12 19.5 19 16 19 11.5V6.5C19 5 12 2.5 12 2.5Z" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M9 11.5L11.5 14L18.5 7.5" stroke="#60a5fa" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
        </div>
        <h1 style="color: #f8fafc; font-size: 2.2rem; font-weight: 700; margin-bottom: 0; line-height: 1.1;">
            SmartKYC Portal
        </h1>
        <p style="color: #64748b; font-size: 0.92rem; margin-top: 6px;">
            Identity Verification & Document Compliance Gateway
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card Container
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        with st.form("password_login_form", border=True):
            username = st.text_input("Username", placeholder="Username")
            password = st.text_input("Password", type="password", placeholder="Password")
            
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            login_btn = st.form_submit_button("Sign In to Portal")
            
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
