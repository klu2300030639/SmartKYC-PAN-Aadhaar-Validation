# SmartKYC - PAN & Aadhaar Validation Web Application

[![Live App](https://img.shields.io/badge/Live-smartkyc--validator.streamlit.app-3b82f6?style=for-the-badge&logo=streamlit)](https://smartkyc-validator.streamlit.app/)

SmartKYC is an enterprise-grade identity document validation web application built with Python, Streamlit, and MySQL/SQLite. It validates the format and mathematical integrity of identity documents (PAN cards and Aadhaar numbers) offline using algorithmic validation (such as the Verhoeff checksum algorithm for Aadhaar numbers).

👉 **Live URL**: **[https://smartkyc-validator.streamlit.app/](https://smartkyc-validator.streamlit.app/)**

---

## 🚀 Features

- **🔒 Password Authentication**: Secure sign-in with BCrypt password hashing.
- **📊 Real-time Dashboard**: Dynamic KPIs, distribution pie charts, validation bar charts, and recent audit trail summaries.
- **💳 PAN Validation**: Checks format compliance (5 letters, 4 digits, 1 letter) and verifies the 4th character entity category (P, C, H, F, A, T, B, L, J, G).
- **🪪 Aadhaar Validation**: Algorithmic integrity verification using the Verhoeff checksum algorithm to prevent manual entry typos and fake IDs.
- **📋 Validation History**: Complete audit trail of validated documents with searching, status filtering (Valid/Invalid), and CSV export. *(Restricted to Admin)*
- **👥 User Management**: CRUD operations for User Accounts, Roles (Admin/User/Guest), and account activation status. *(Restricted to Admin)*
- **🔍 System Audit Logs**: Administrative module to inspect user actions, modules modified, actions taken, and accurate system timestamps. *(Restricted to Admin)*
- **⚙️ Preferences & Configurations**: Read-only database connection settings, connectivity testing, and administrative data purge tools.

---

## 💾 Zero-Config Database (MySQL & SQLite)

The application supports a **transparent dual-driver database wrapper** in `db.py`:
- **Local Fallback**: If MySQL settings are not configured or are unreachable, the system automatically initializes a local SQLite file database (`kyc_validator.db`) right inside the workspace.
- **Auto-Initialization**: On the first launch, the driver automatically creates all required tables and seeds the default **System Administrator** (`admin` / `admin123`) account.
- **Multi-Cloud Ready**: Perfect for Streamlit Community Cloud where external MySQL databases are unavailable.

---

## 🛠 Tech Stack

- **Frontend & Backend**: Streamlit (Python)
- **Database**: MySQL 8.0+ / SQLite 3
- **Security**: BCrypt hashing for secure credential storage
- **Data & Visualizations**: Pandas, Plotly Express
- **Keep Awake**: GitHub Actions Ping Workflow (runs every 30 minutes to prevent container sleep)

---

## ⚙️ How to Configure and Run Locally

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Configure Database (Optional)
If you want to use MySQL, create a `.env` file in the root directory based on `.env.example`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=KYCValidatorDB
DB_USER=root
DB_PASSWORD=root
```
*If no `.env` file is present, the app will gracefully run using the built-in SQLite database.*

### 3. Run the Application
Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```
The app will be available in your browser at `http://localhost:8501`.

---

## ☁️ Deployment on Streamlit Cloud

To deploy this application to Streamlit Community Cloud:

1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. Select this repository, the branch (`main`), and set `streamlit_app.py` as the main entrypoint file.
4. **Deploy instantly**! The app will automatically initialize a SQLite database in the cloud.
5. *(Optional)* If you wish to use a persistent cloud MySQL database, add your database credentials in the **Secrets** settings panel using TOML:
   ```toml
   DB_HOST = "your-cloud-db-host.com"
   DB_PORT = 3306
   DB_DATABASE = "KYCValidatorDB"
   DB_USER = "your_db_user"
   DB_PASSWORD = "your_db_password"
   ```

---

## ⚡ Keep-Alive Cronjob
To prevent Streamlit Community Cloud from putting this free app to sleep after inactivity, a GitHub Action is configured in `.github/workflows/keep_alive.yml`. It pings the live URL (`https://smartkyc-validator.streamlit.app/`) every 30 minutes to keep the container active and warm 24/7.