"""
Database Engine & Session Management Layer using SQLAlchemy.
Supports automatic dual-driver fallback: Production MySQL or Zero-Config SQLite.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Check Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_DATABASE = os.getenv("DB_DATABASE", "KYCValidatorDB")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

# Determine Connection URL
engine = None
DB_TYPE = "sqlite"

if os.getenv("FORCE_SQLITE") != "1":
    try:
        mysql_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        test_engine = create_engine(mysql_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        with test_engine.connect() as conn:
            pass
        engine = test_engine
        DB_TYPE = "mysql"
    except Exception:
        engine = None

if engine is None:
    DB_TYPE = "sqlite"
    sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "kyc_validator.db"))
    engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI Dependency for database session injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initializes tables and seeds initial administrator accounts."""
    from app.models.user import User
    from app.models.validation import ValidationHistory
    from app.models.audit_log import AuditLog
    from app.models.settings import ApplicationSetting
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed ADMIN
        admin_user = db.query(User).filter((User.username == 'ADMIN') | (User.username == 'admin')).first()
        if not admin_user:
            admin_user = User(
                full_name="System Administrator",
                username="ADMIN",
                email="admin@smartkyc.com",
                password_hash="$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva",
                phone="+1234567890",
                role="Admin",
                status="Active"
            )
            db.add(admin_user)
        else:
            admin_user.username = "ADMIN"
            admin_user.password_hash = "$2b$10$aTdvtkOadKHMNjT5brkqmeOLF8CKLdYinhmzHd.XN9omRNklr2hva"
            
        # Seed Sindiri (password: Aryan@AS_1622)
        sindiri_user = db.query(User).filter((User.username == 'Sindiri') | (User.email == 'aryansindiri115714@gmail.com')).first()
        if not sindiri_user:
            sindiri_user = User(
                full_name="Aryan Sindiri",
                username="Sindiri",
                email="aryansindiri115714@gmail.com",
                password_hash="$2b$10$g4izTwI0z7zsuhABJQ.ypeqy6MhtjQ5/gU1gYEaCFgJKORNmkVoKG",
                phone="7683904679",
                role="Admin",
                status="Active"
            )
            db.add(sindiri_user)
        else:
            sindiri_user.username = "Sindiri"
            sindiri_user.password_hash = "$2b$10$g4izTwI0z7zsuhABJQ.ypeqy6MhtjQ5/gU1gYEaCFgJKORNmkVoKG"
            sindiri_user.role = "Admin"
            
        # Seed Aryan
        aryan_user = db.query(User).filter((User.username == 'Aryan') | (User.email == 'aryansindiri9876@gmail.com')).first()
        if not aryan_user:
            aryan_user = User(
                full_name="Sindiri",
                username="Aryan",
                email="aryansindiri9876@gmail.com",
                password_hash="$2b$10$aTvNsqJzjwPJSAD78.X0..IcBpwBejYABcSOd6v8XgZfxxvxSD0DK",
                phone="9861395454",
                role="Admin",
                status="Active"
            )
            db.add(aryan_user)
        else:
            aryan_user.role = "Admin"
            
        # Seed Application Settings
        default_settings = [
            ("theme", "dark"),
            ("validation_cleanup_days", "30"),
            ("max_failed_attempts", "5")
        ]
        for key, val in default_settings:
            existing = db.query(ApplicationSetting).filter(ApplicationSetting.setting_key == key).first()
            if not existing:
                db.add(ApplicationSetting(setting_key=key, setting_value=val))
                
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
