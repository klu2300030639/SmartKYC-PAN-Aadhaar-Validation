import mysql.connector
from mysql.connector import pooling
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# We use connection pooling to avoid reconnecting on every page reload
_connection_pool = None

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

def get_pool():
    global _connection_pool
    if _connection_pool is None:
        try:
            config = get_connection_config()
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="smartkyc_pool",
                pool_size=5,
                pool_reset_session=True,
                **config
            )
        except Exception as e:
            st.error(f"Database connection pool initialization failed: {e}")
            raise e
    return _connection_pool

def get_connection():
    conn = None
    try:
        conn = get_pool().get_connection()
    except Exception:
        # Fallback to direct connection if pool fails
        config = get_connection_config()
        conn = mysql.connector.connect(**config)
    
    # Guarantee that the connection is active by pinging and reconnecting if necessary
    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except Exception as e:
        # If ping/reconnect fails, try one more direct reconnect
        config = get_connection_config()
        conn = mysql.connector.connect(**config)
        
    return conn

def execute_query(query, params=None, fetch=False, commit=False):
    """
    Executes a query and safely releases the connection back to the pool.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    result = None
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
