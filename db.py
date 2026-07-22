import mysql.connector
from mysql.connector import pooling
import sqlite3
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# We use connection pooling to avoid reconnecting on every page reload
_connection_pool = None
DB_TYPE = "mysql"  # Can be "mysql" or "sqlite"

def get_connection_config():
    # If deploying on Streamlit Cloud, st.secrets will contain configuration
    try:
        # Support flat environment-like naming in st.secrets
        if "DB_HOST" in st.secrets:
            return {
                "host": st.secrets.get("DB_HOST"),
                "port": int(st.secrets.get("DB_PORT", 3306)),
                "database": st.secrets.get("DB_DATABASE", "KYCValidatorDB"),
                "user": st.secrets.get("DB_USER", "root"),
                "password": st.secrets.get("DB_PASSWORD", "")
            }
        # Support nested [db] format
        elif "db" in st.secrets:
            return {
                "host": st.secrets.db.get("host", "localhost"),
                "port": int(st.secrets.db.get("port", 3306)),
                "database": st.secrets.db.get("database", "KYCValidatorDB"),
                "user": st.secrets.db.get("username", "root"),
                "password": st.secrets.db.get("password", "root")
            }
    except Exception:
        pass
    # Otherwise use local environment variables or defaults
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "database": os.getenv("DB_DATABASE", "KYCValidatorDB"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root")
    }

def init_sqlite_db(conn):
    cursor = conn.cursor()
    # Create tables in SQLite if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT,
        role TEXT DEFAULT 'User' NOT NULL,
        status TEXT DEFAULT 'Active' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS validation_history (
        validation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        document_type TEXT NOT NULL,
        document_number TEXT NOT NULL,
        status TEXT NOT NULL,
        reason TEXT,
        validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        module TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        login_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout_time TIMESTAMP NULL,
        login_status TEXT NOT NULL,
        ip_address TEXT,
        device_name TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS application_settings (
        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL
    )
    """)
    
    # Seed default Admin User (username: admin, password: admin123)
    cursor.execute("SELECT user_id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (full_name, username, email, password_hash, phone, role, status)
        VALUES ('System Administrator', 'admin', 'admin@smartkyc.com', '$2a$10$c8hw293ufpUCB.FROSMyAOVRKGGmxdW62.3NoFWoy/ZIHipF8/2tq', '+1234567890', 'Admin', 'Active')
        """)
        
    # Seed initial application settings
    cursor.execute("SELECT setting_id FROM application_settings")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('theme', 'dark')")
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('validation_cleanup_days', '30')")
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('max_failed_attempts', '5')")
        
    conn.commit()
    cursor.close()

def get_pool():
    global _connection_pool, DB_TYPE
    if DB_TYPE == "sqlite":
        return None
    if _connection_pool is None:
        try:
            config = get_connection_config()
            
            # Detect Streamlit Cloud deployment environment
            is_cloud = os.path.exists('/mount/src') or os.getenv("STREAMLIT_SHARING_AUTHOR_KEY") is not None
            # If we are on Streamlit Cloud and the host is localhost, immediately fallback to SQLite to avoid connection timeouts
            if is_cloud and config.get("host") in ("localhost", "127.0.0.1"):
                DB_TYPE = "sqlite"
                return None
                
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="smartkyc_pool",
                pool_size=5,
                pool_reset_session=True,
                **config
            )
        except Exception:
            DB_TYPE = "sqlite"
            return None
    return _connection_pool

def get_connection():
    global DB_TYPE
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect("kyc_validator.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        init_sqlite_db(conn)
        return conn
        
    try:
        pool = get_pool()
        if DB_TYPE == "sqlite":
            return get_connection()
        conn = pool.get_connection()
    except Exception:
        # Fallback to direct MySQL connection
        try:
            config = get_connection_config()
            conn = mysql.connector.connect(**config)
        except Exception:
            DB_TYPE = "sqlite"
            return get_connection()
            
    # Guarantee active connection
    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except Exception:
        try:
            config = get_connection_config()
            conn = mysql.connector.connect(**config)
        except Exception:
            DB_TYPE = "sqlite"
            return get_connection()
            
    return conn

def execute_query(query, params=None, fetch=False, commit=False):
    """
    Executes a query and safely releases the connection back to the database.
    Supports both MySQL and SQLite transparently.
    """
    global DB_TYPE
    conn = get_connection()
    result = None
    
    if DB_TYPE == "sqlite":
        # Translate placeholder %s to SQLite style ?
        query = query.replace("%s", "?")
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
            elif fetch:
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    else:
        cursor = conn.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
            elif fetch:
                result = cursor.fetchall()
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    return result

def check_db_connection():
    """
    Checks if connection can be established.
    """
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False
