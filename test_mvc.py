"""
Automated Test Suite for SmartKYC MVC Architecture.
"""
import pytest
from starlette.testclient import TestClient
from app.main import app
from app.database import init_db
from app.services.verhoeff import validate_aadhaar, validate_verhoeff
from app.services.pan_validator import validate_pan

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()


def test_verhoeff_algorithm():
    # Valid Aadhaar numbers
    assert validate_verhoeff("200000000003") is True
    assert validate_verhoeff("200000000004") is False  # Invalid checksum
    
    # Validation Service
    assert validate_aadhaar("2000 0000 0003")["valid"] is True
    assert validate_aadhaar("0200 0000 0003")["valid"] is False  # Cannot start with 0
    assert validate_aadhaar("123")["valid"] is False  # Too short



def test_pan_validator():
    # Valid PAN
    res = validate_pan("ABCPC1234F")
    assert res["valid"] is True
    assert res["entity_type"] == "Individual / Person"
    assert res["surname_initial"] == "C"
    
    # Invalid PAN
    assert validate_pan("INVALID")["valid"] is False
    assert validate_pan("ABCPC12345")["valid"] is False  # Missing last letter



def test_auth_and_protected_endpoints():
    # 1. Invalid Login
    res = client.post("/api/auth/login", json={"username": "wrong", "password": "wrong"})
    assert res.status_code == 401
    
    # 2. Valid Login as ADMIN
    res = client.post("/api/auth/login", json={"username": "ADMIN", "password": "ADMIN"})
    assert res.status_code == 200
    user_data = res.json()
    assert user_data["username"] == "ADMIN"
    assert user_data["role"] == "Admin"
    
    # Session cookie is saved in test client
    # 3. Access Protected /api/auth/me
    res = client.get("/api/auth/me")
    assert res.status_code == 200
    assert res.json()["username"] == "ADMIN"
    
    # 4. Perform PAN validation API
    res = client.post("/api/validate/pan", json={"pan_number": "ABCPC1234F"})
    assert res.status_code == 200
    assert res.json()["valid"] is True
    
    # 5. Perform Aadhaar validation API
    res = client.post("/api/validate/aadhaar", json={"aadhaar_number": "2000 0000 0003"})
    assert res.status_code == 200
    assert res.json()["valid"] is True

    
    # 6. Check Dashboard Stats API
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    assert res.json()["total_validations"] >= 2
    
    # 7. Check KYC History API
    res = client.get("/api/history")
    assert res.status_code == 200
    assert len(res.json()) >= 2
    
    # 8. Check History CSV Export API
    res = client.get("/api/history/export")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    
    # 9. Check Users List API
    res = client.get("/api/users")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    
    # 10. Check Audit Logs API
    res = client.get("/api/audit")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    
    # 11. Logout
    res = client.post("/api/auth/logout")
    assert res.status_code == 200


def test_sindiri_login():
    res = client.post("/api/auth/login", json={"username": "Sindiri", "password": "Aryan@AS_1622"})
    assert res.status_code == 200
    assert res.json()["username"] == "Sindiri"
    assert res.json()["role"] == "Admin"
    client.post("/api/auth/logout")
