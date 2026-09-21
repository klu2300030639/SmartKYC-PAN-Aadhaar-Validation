import mysql.connector
from mysql.connector import pooling
import sqlite3
import os
import socket
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_connection_pool = None
_sqlite_initialized = False
DB_TYPE = None  # Resolved dynamically: "mysql" or "sqlite"

def get_connection_config():
    """Extracts database configuration from st.secrets or environment variables."""
    try:
        if hasattr(st, "secrets") and st.secrets:
            if "DB_HOST" in st.secrets:
                return {
                    "host": st.secrets.get("DB_HOST"),
                    "port": int(st.secrets.get("DB_PORT", 3306)),
                    "database": st.secrets.get("DB_DATABASE", "KYCValidatorDB"),
                    "user": st.secrets.get("DB_USER", "root"),
                    "password": st.secrets.get("DB_PASSWORD", "")
                }
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
        
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "database": os.getenv("DB_DATABASE", "KYCValidatorDB"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root")
    }

def is_socket_reachable(host: str, port: int, timeout: float = 0.5) -> bool:
    """Quick non-blocking probe to verify if a TCP port is open."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except Exception:
        return False

def init_sqlite_db(conn):
    """Initializes SQLite schema and seeds default accounts once."""
    global _sqlite_initialized
    if _sqlite_initialized:
        return
        
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    
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
    
    # Seed default Admin User (username: ADMIN, password: ADMIN)
    cursor.execute("SELECT user_id FROM users WHERE username = 'ADMIN'")
    if not cursor.fetchone():
        cursor.execute("SELECT user_id FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            cursor.execute("UPDATE users SET username = 'ADMIN', password_hash = '$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva' WHERE username = 'admin'")
        else:
            cursor.execute("SELECT user_id FROM users WHERE email = 'admin@smartkyc.com'")
            if cursor.fetchone():
                cursor.execute("UPDATE users SET username = 'ADMIN', password_hash = '$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva' WHERE email = 'admin@smartkyc.com'")
            else:
                cursor.execute("""
                INSERT INTO users (full_name, username, email, password_hash, phone, role, status)
                VALUES ('System Administrator', 'ADMIN', 'admin@smartkyc.com', '$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva', '+1234567890', 'Admin', 'Active')
                """)
        
    # Seed Sindiri User (username: Sindiri, password: Aryan@AS_1622)
    cursor.execute("SELECT user_id FROM users WHERE username = 'Sindiri'")
    if not cursor.fetchone():
        cursor.execute("SELECT user_id FROM users WHERE email = 'aryansindiri115714@gmail.com'")
        if cursor.fetchone():
            cursor.execute("UPDATE users SET username = 'Sindiri', password_hash = '$2b$10$g4izTwI0z7zsuhABJQ.ypeqy6MhtjQ5/gU1gYEaCFgJKORNmkVoKG', role = 'Admin' WHERE email = 'aryansindiri115714@gmail.com'")
        else:
            cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, phone, role, status)
            VALUES ('Aryan Sindiri', 'Sindiri', 'aryansindiri115714@gmail.com', '$2b$10$g4izTwI0z7zsuhABJQ.ypeqy6MhtjQ5/gU1gYEaCFgJKORNmkVoKG', '7683904679', 'Admin', 'Active')
            """)
            
    # Seed Aryan User (username: Aryan)
    cursor.execute("SELECT user_id FROM users WHERE username = 'Aryan'")
    if not cursor.fetchone():
        cursor.execute("SELECT user_id FROM users WHERE email = 'aryansindiri9876@gmail.com'")
        if cursor.fetchone():
            cursor.execute("UPDATE users SET username = 'Aryan', password_hash = '$2b$10$aTvNsqJzjwPJSAD78.X0..IcBpwBejYABcSOd6v8XgZfxxvxSD0DK', role = 'Admin' WHERE email = 'aryansindiri9876@gmail.com'")
        else:
            cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, phone, role, status)
            VALUES ('Sindiri', 'Aryan', 'aryansindiri9876@gmail.com', '$2b$10$aTvNsqJzjwPJSAD78.X0..IcBpwBejYABcSOd6v8XgZfxxvxSD0DK', '9861395454', 'Admin', 'Active')
            """)
            
    # Seed initial settings
    cursor.execute("SELECT setting_id FROM application_settings")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('theme', 'dark')")
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('validation_cleanup_days', '30')")
        cursor.execute("INSERT INTO application_settings (setting_key, setting_value) VALUES ('max_failed_attempts', '5')")
        
    conn.commit()
    cursor.close()
    _sqlite_initialized = True

def resolve_db_type():
    """Determines whether to use MySQL or SQLite without blocking the runtime."""
    global DB_TYPE
    if DB_TYPE is not None:
        return DB_TYPE
        
    if os.getenv("FORCE_SQLITE") == "1":
        DB_TYPE = "sqlite"
        return DB_TYPE
        
    config = get_connection_config()
    host = config.get("host", "localhost")
    port = config.get("port", 3306)
    
    # If host is localhost/127.0.0.1, check if MySQL port is actually listening locally
    if host in ("localhost", "127.0.0.1"):
        if not is_socket_reachable(host, port, timeout=0.3):
            # No local MySQL running (e.g. Cloud container or non-MySQL dev machine)
            DB_TYPE = "sqlite"
            return DB_TYPE
            
    # External host or active local socket: attempt brief connection test
    try:
        conn = mysql.connector.connect(connection_timeout=2, **config)
        conn.close()
        DB_TYPE = "mysql"
    except Exception:
        DB_TYPE = "sqlite"
        
    return DB_TYPE

def get_pool():
    global _connection_pool
    if resolve_db_type() == "sqlite":
        return None
        
    if _connection_pool is None:
        try:
            config = get_connection_config()
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="smartkyc_pool",
                pool_size=5,
                pool_reset_session=True,
                connection_timeout=3,
                **config
            )
        except Exception:
            global DB_TYPE
            DB_TYPE = "sqlite"
            return None
    return _connection_pool

def get_connection():
    """Returns an active database connection (MySQL or SQLite)."""
    if resolve_db_type() == "sqlite":
        sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "kyc_validator.db"))
        conn = sqlite3.connect(sqlite_path, check_same_thread=False, timeout=10.0)
        conn.row_factory = sqlite3.Row
        init_sqlite_db(conn)
        return conn
        
    try:
        pool = get_pool()
        if pool is not None:
            conn = pool.get_connection()
            conn.ping(reconnect=True, attempts=2, delay=1)
            return conn
    except Exception:
        pass
        
    # Fallback to direct MySQL connection or SQLite
    try:
        config = get_connection_config()
        conn = mysql.connector.connect(connection_timeout=2, **config)
        return conn
    except Exception:
        global DB_TYPE
        DB_TYPE = "sqlite"
        return get_connection()

def execute_query(query, params=None, fetch=False, commit=False):
    """
    Executes a query and safely releases the connection back to the database.
    Supports both MySQL and SQLite transparently.
    """
    conn = get_connection()
    result = None
    
    try:
        if resolve_db_type() == "sqlite":
            query_sqlite = query.replace("%s", "?")
            cursor = conn.cursor()
            try:
                cursor.execute(query_sqlite, params or ())
                if commit:
                    conn.commit()
                    result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
                elif fetch:
                    rows = cursor.fetchall()
                    result = [dict(row) for row in rows]
            finally:
                cursor.close()
        else:
            cursor = conn.cursor(dictionary=True, buffered=True)
            try:
                cursor.execute(query, params or ())
                if commit:
                    conn.commit()
                    result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
                elif fetch:
                    result = cursor.fetchall()
            finally:
                cursor.close()
    except Exception as e:
        if commit:
            try:
                conn.rollback()
            except Exception:
                pass
        raise e
    finally:
        try:
            conn.close()
        except Exception:
            pass
            
    return result

def check_db_connection():
    """Checks if database connection is functional."""
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False
