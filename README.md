# SmartKYC - PAN & Aadhaar Validation Web Application

SmartKYC is an enterprise-grade document validation web application built with Streamlit, Python, and MySQL. It verifies the format and mathematical integrity of identity documents (PAN cards and Aadhaar numbers) offline using algorithmic validation (such as the Verhoeff checksum algorithm for Aadhaar numbers).

---

## 🚀 Features

- **🔐 Secure Login & Sign In**: Robust authentication with BCrypt password hashing.
- **📊 Real-time Dashboard**: Dynamic KPIs, distribution pie charts, validation bar charts, and recent audit trail summaries.
- **💳 PAN Validation**: Checks format compliance (5 letters, 4 digits, 1 letter) and verifies the 4th character entity category (P, C, H, F, A, T, B, L, J, G).
- **🪪 Aadhaar Validation**: Algorithmic integrity verification using the Verhoeff checksum algorithm to prevent manual entry typos and fake IDs.
- **📋 Validation History**: Complete audit trail of validated documents with searching, status filtering (Valid/Invalid), and CSV export.
- **👥 User Management**: Complete CRUD operations for User Accounts, Roles (Admin/User), and account activation status.
- **🔍 System Audit Logs**: Administrative module to inspect user actions, modules modified, actions taken, and accurate system timestamps.
- **⚙️ Preferences & Configurations**: Toggle between a premium Banking Dark Theme and Light Theme, view read-only database connections, test connectivity, and clear history/audit tables.

---

## 🛠 Tech Stack

- **Frontend & Backend**: Streamlit (Python)
- **Database**: MySQL 8.0+
- **Security**: BCrypt hashing for secure credential storage
- **Data & Visualizations**: Pandas, Plotly Express

---

## 📂 Database Schema Setup

The database schema and initial setup are described in `database.sql`. To set up the database locally:

1. Start your local MySQL service.
2. Execute the schema configuration:
   ```bash
   mysql -u root -p < database.sql
   ```
3. A default admin user will be seeded:
   - **Username**: `admin`
   - **Password**: `admin123`

---

## ⚙️ How to Configure and Run Locally

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file in the root directory based on `.env.example`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=KYCValidatorDB
DB_USER=root
DB_PASSWORD=root
```

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
3. Select this repository, the branch, and set `streamlit_app.py` as the main entry point file.
4. Expand **Advanced settings** and define your database credentials in **Secrets** using TOML:
   ```toml
   [db]
   host = "your-cloud-db-host.com"
   port = 3306
   database = "KYCValidatorDB"
   username = "your_db_user"
   password = "your_db_password"
   ```
5. Click **Deploy!**