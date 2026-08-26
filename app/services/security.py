"""
Security & Cryptography Service.
Handles BCrypt password hashing, verification, and session token generation.
"""
import os
import secrets
import bcrypt

SECRET_KEY = os.getenv("SECRET_KEY", "smartkyc_super_secret_jwt_key_2026")


def hash_password(password: str) -> str:
    """Hash a plaintext password with BCrypt."""
    salt = bcrypt.gensalt(10)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored BCrypt hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def generate_session_token() -> str:
    """Generates a secure cryptographic random token."""
    return secrets.token_hex(32)
