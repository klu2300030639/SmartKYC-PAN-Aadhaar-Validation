<div align="center">
  <img src="smartkyc_banner.jpg" alt="SmartKYC Banner" width="100%">
  
  # 🛡️ SmartKYC — Identity Verification Web App
  
  [![Live App](https://img.shields.io/badge/Live-smartkyc--validator.streamlit.app-3b82f6?style=for-the-badge&logo=streamlit)](https://smartkyc-validator.streamlit.app/)
  [![GitHub License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://python.org)
  
  **A premium, enterprise-grade identity document validation engine. Validates PAN & Aadhaar structures offline using mathematical integrity checks (such as the Verhoeff checksum algorithm).**
  
  🔗 **Access Deployed Website**: **[smartkyc-validator.streamlit.app](https://smartkyc-validator.streamlit.app/)**
</div>

---

## ✨ Features

### 🔐 Secure Gateways
- **Credential Sign-In**: Form-based authentication with **BCrypt** password hashing. Supports instant `Enter` key submission.
- **Gmail OTP Login**: Toggle option for logging in via dynamic 6-digit email codes (Gmail SMTP), with a fallback developer debug mode.

### 💳 Document Validators (Offline)
- **PAN Verification**: Format verification matching the standard regex category rules. Validates category holders (Private, Government, Trust, etc.).
- **Aadhaar Verification**: Strict offline integrity checks using the **Verhoeff matrix multiplication algorithm** to prevent typos and invalid cards.

### 📊 Dashboard & Monitoring
- **Real-Time Metrics**: Visual indicators for total validations, success ratios, and verification distributions using **Plotly Express** charts.
- **User Administration**: Strict CRUD tools for creating, suspending, or permanently deleting user accounts.
- **System Audit Trail**: Complete log database tracking modules accessed, timestamps, actions, and security levels. *(Admins only)*

---

## 💾 Zero-Config Database Architecture

SmartKYC is equipped with a **transparent dual-driver database adapter** in [db.py](db.py):

- **SQLite Fallback (Cloud & Dev)**: If no MySQL credentials are provided (or if you deploy the app to Streamlit Cloud), the system automatically initializes a local SQLite file (`kyc_validator.db`) and seeds it with tables and default admin credentials.
- **Production MySQL**: Switch instantly to a persistent external MySQL service by simply filling in your environment variables.

---

## 🛠️ Tech Stack

- **Framework**: Streamlit (Python)
- **Database Engine**: MySQL 8.0+ / SQLite 3
- **Data & Charts**: Pandas, Plotly Express
- **Security & Encription**: BCrypt, hashlib
- **Keep-Alive Daemon**: GitHub Actions automated runner (runs every 30 minutes to prevent container sleep)

---

## 🚀 Local Quickstart

### 1. Clone & Install Dependencies
Make sure you have Python 3.9+ installed:
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run streamlit_app.py
```
*No database configuration is required! The application will automatically create a local `kyc_validator.db` file and seed the default **Admin** account:*
- **Username**: `admin`
- **Password**: `admin123`

---

## ⚙️ Advanced Settings (MySQL Setup)

To use a persistent MySQL database instead of the SQLite fallback, create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=KYCValidatorDB
DB_USER=root
DB_PASSWORD=root
```

---

## ⚡ Deployment & Keep-Warm

The app is configured to run **24/7** on Streamlit Community Cloud. A keep-awake cronjob workflow is active in `.github/workflows/keep_alive.yml`, automatically pinging the public URL every 30 minutes to prevent the container from going to sleep during periods of inactivity.