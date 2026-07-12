# SmartKYC - PAN & Aadhaar Validation Desktop Application

SmartKYC is an enterprise-grade offline document validation desktop application built with JavaFX, Maven, and MySQL. It verifies the format and mathematical integrity of identity documents (PAN cards and Aadhaar numbers) offline using algorithmic validation (such as the Verhoeff checksum algorithm for Aadhaar numbers).

## 🚀 Features

- **🔐 Secure Login & Sign In**: Robust authentication with BCrypt password hashing.
- **📊 Real-time Dashboard**: Dynamic KPIs, distribution pie charts, validation bar charts, and recent audit trail summaries.
- **💳 PAN Validation**: Checks format compliance (5 letters, 4 digits, 1 letter) and verifies the 4th character entity category (P, C, H, F, A, T, B, L, J, G).
- **🪪 Aadhaar Validation**: Algorithmic integrity verification using the Verhoeff checksum algorithm to prevent manual entry typos and fake IDs.
- **📋 Validation History**: Complete audit trail of validated documents with searching, status filtering (Valid/Invalid), single-row deletion, and CSV export.
- **👥 User Management**: Complete CRUD operations for User Accounts, Roles (Admin/User), and account activation status.
- **🔍 System Audit Logs**: Administrative module to inspect user actions, modules modified, actions taken, and accurate system timestamps.
- **⚙️ Preferences & Configurations**: Toggle between a premium Banking Dark Theme and Light Theme, view read-only database connections, test connectivity, and clear history/audit tables.

---

## 🛠 Tech Stack

- **Frontend**: JavaFX 21 (FXML layouts + Vanilla CSS)
- **Backend Core**: Java 17
- **Build Tool**: Maven 3.9+
- **Database**: MySQL 8.0+
- **Security**: BCrypt hashing for secure credential storage

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

## ⚙️ How to Configure and Run

### 1. Configure Connection Properties
Update the database connection properties in:
`src/main/resources/config.properties`
```properties
db.url=jdbc:mysql://localhost:3306/KYCValidatorDB?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
db.username=root
db.password=root
```

### 2. Compile and Build
Clean and compile all Maven dependencies and Java modules:
```bash
mvn clean compile
```

### 3. Package into a JAR
Build the final executable JAR:
```bash
mvn package -DskipTests
```
The final package will be generated at:
`target/smartkyc-validator-1.0.0.jar`

### 4. Run the Application
Execute the JavaFX application directly:
```bash
mvn javafx:run
```