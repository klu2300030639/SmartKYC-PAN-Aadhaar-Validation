-- database.sql - Schema configuration for KYCValidatorDB

CREATE DATABASE IF NOT EXISTS KYCValidatorDB;
USE KYCValidatorDB;

DROP TABLE IF EXISTS application_settings;
DROP TABLE IF EXISTS login_history;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS validation_history;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'User' NOT NULL,
    status VARCHAR(20) DEFAULT 'Active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE validation_history (
    validation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    document_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    reason VARCHAR(255),
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    module VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE login_history (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    login_status VARCHAR(20) NOT NULL,
    ip_address VARCHAR(45),
    device_name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE application_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) UNIQUE NOT NULL,
    setting_value VARCHAR(255) NOT NULL
);

INSERT INTO application_settings (setting_key, setting_value) VALUES
('theme', 'dark'),
('validation_cleanup_days', '30'),
('max_failed_attempts', '5');

-- Seed Admin User (username: ADMIN, password: ADMIN)
-- BCrypt Hash: $2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva (standard BCrypt hash for ADMIN)
INSERT INTO users (full_name, username, email, password_hash, phone, role, status) VALUES
('System Administrator', 'ADMIN', 'admin@smartkyc.com', '$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva', '+1234567890', 'Admin', 'Active');

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_validation_document ON validation_history(document_number);
CREATE INDEX idx_validation_status ON validation_history(status);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_login_user ON login_history(user_id);
