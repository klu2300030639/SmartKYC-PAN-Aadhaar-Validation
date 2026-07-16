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
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0; text-align: center; margin-bottom: 24px;'>Secure Authentication</h3>", unsafe_allow_html=True)
            
            username = st.text_input("Username", key="login_username_field", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password_field", placeholder="Enter your password")
            
            st.markdown("<div style='margin-top: 24px;'>", unsafe_allow_html=True)
            login_btn = st.button("Log In", key="login_submit_btn")
            st.markdown("</div>", unsafe_allow_html=True)
            
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

if __name__ == "__main__":
    show_login()
