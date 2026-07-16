import bcrypt
import streamlit as st
import socket
from datetime import datetime
import db

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    # bcrypt in python requires bytes
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Store as string (matches $2a$ format)
    # We replace b'$2b$' with '$2a$' if needed, but python bcrypt generates $2b$ which is compatible.
    # The database has $2a$. Python's checkpw supports checking $2a$ hashes.
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    try:
        # Standard bcrypt verify
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_client_details():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address, hostname
    except Exception:
        return "127.0.0.1", "Unknown"

def login(username, password):
    query = "SELECT user_id, full_name, username, email, password_hash, role, status FROM users WHERE username = %s"
    users = db.execute_query(query, (username,), fetch=True)
    
    ip_addr, device = get_client_details()
    
    if not users:
        # User not found
        # Insert audit log
        log_audit(None, "LOGIN_FAILED", "Authentication", f"Failed login attempt for username: {username} (User not found)")
        return False, "Invalid username or password"
        
    user = users[0]
    
    if user['status'] != 'Active':
        log_audit(user['user_id'], "LOGIN_FAILED", "Authentication", f"Failed login attempt for {username} (Account suspended)")
        return False, f"Account is {user['status']}. Please contact administrator."
        
    # Check password
    if check_password(password, user['password_hash']):
        # Insert into login_history
        login_query = """
            INSERT INTO login_history (user_id, login_status, ip_address, device_name)
            VALUES (%s, 'Success', %s, %s)
        """
        login_id = db.execute_query(login_query, (user['user_id'], ip_addr, device), commit=True)
        
        # Log audit
        log_audit(user['user_id'], "LOGIN_SUCCESS", "Authentication", f"Logged in from {ip_addr} ({device})")
        
        # Save session
        st.session_state.logged_in = True
        st.session_state.user_id = user['user_id']
        st.session_state.username = user['username']
        st.session_state.full_name = user['full_name']
        st.session_state.role = user['role']
        st.session_state.login_id = login_id
        
        return True, "Login successful"
    else:
        # Insert into login_history as failed
        login_query = """
            INSERT INTO login_history (user_id, login_status, ip_address, device_name)
            VALUES (%s, 'Failed', %s, %s)
        """
        db.execute_query(login_query, (user['user_id'], ip_addr, device), commit=True)
        
        # Log audit
        log_audit(user['user_id'], "LOGIN_FAILED", "Authentication", f"Failed password attempt for username: {username}")
        return False, "Invalid username or password"

def logout():
    if getattr(st.session_state, 'logged_in', False):
        user_id = st.session_state.get('user_id')
        login_id = st.session_state.get('login_id')
        
        # Update logout time in login_history
        if login_id:
            logout_query = "UPDATE login_history SET logout_time = %s WHERE login_id = %s"
            db.execute_query(logout_query, (datetime.now(), login_id), commit=True)
            
        log_audit(user_id, "LOGOUT", "Authentication", f"User {st.session_state.get('username')} logged out")
        
    # Clear session state
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.role = None
    st.session_state.login_id = None

def log_audit(user_id, action, module, description):
    query = """
        INSERT INTO audit_logs (user_id, action, module, description)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute_query(query, (user_id, action, module, description), commit=True)
    except Exception as e:
        # Print error or log to file but don't crash the request
        print(f"Failed to log audit: {e}")

def login_via_email(email_addr):
    query = "SELECT user_id, full_name, username, email, role, status FROM users WHERE email = %s"
    users = db.execute_query(query, (email_addr,), fetch=True)
    
    ip_addr, device = get_client_details()
    
    if not users:
        # User not found
        log_audit(None, "LOGIN_FAILED_OTP", "Authentication", f"Failed OTP login for email: {email_addr} (Email not found)")
        return False, "This email is not registered. Please create an account first."
        
    user = users[0]
    
    if user['status'] != 'Active':
        log_audit(user['user_id'], "LOGIN_FAILED_OTP", "Authentication", f"Failed OTP login for {email_addr} (Account suspended)")
        return False, f"Account is {user['status']}. Please contact administrator."
        
    # Create session history
    login_query = """
        INSERT INTO login_history (user_id, login_status, ip_address, device_name)
        VALUES (%s, 'Success', %s, %s)
    """
    login_id = db.execute_query(login_query, (user['user_id'], ip_addr, device), commit=True)
    
    log_audit(user['user_id'], "LOGIN_SUCCESS_OTP", "Authentication", f"Logged in via Gmail OTP from {ip_addr} ({device})")
    
    # Save session
    st.session_state.logged_in = True
    st.session_state.user_id = user['user_id']
    st.session_state.username = user['username']
    st.session_state.full_name = user['full_name']
    st.session_state.role = user['role']
    st.session_state.login_id = login_id
    
    return True, "Login successful"

