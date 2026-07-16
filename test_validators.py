import pytest
import validators

def test_validate_pan_valid():
    # Individual PAN (P in 4th char is valid)
    res = validators.validate_pan("ABCPD1234F")
    assert res.valid is True
    assert res.normalized_input == "ABCPD1234F"
    
    # Company PAN (C in 4th char is valid)
    res = validators.validate_pan("ABCCc1234z")
    assert res.valid is True
    assert res.normalized_input == "ABCCC1234Z"

def test_validate_pan_invalid_format():
    # Wrong length
    res = validators.validate_pan("ABCPE1234")
    assert res.valid is False
    assert "character" in res.reason.lower()
    
    # Wrong characters
    res = validators.validate_pan("ABC1P1234F")
    assert res.valid is False
    assert "format invalid" in res.reason.lower()

def test_validate_pan_invalid_category():
    # 'X' is not a valid 4th category character
    res = validators.validate_pan("ABCDX1234F")
    assert res.valid is False
    assert "4th character" in res.reason.lower()

def test_validate_aadhaar_valid():
    # Valid Aadhaar with correct Verhoeff checksum
    res = validators.validate_aadhaar("200000000003")
    assert res.valid is True

def test_validate_aadhaar_invalid():
    # Incorrect length
    res = validators.validate_aadhaar("1234567")
    assert res.valid is False
    
    # Starts with 0 or 1
    res = validators.validate_aadhaar("023456789012")
    assert res.valid is False
    
    # Incorrect checksum
    res = validators.validate_aadhaar("200000000004")
    assert res.valid is False
    assert "checksum" in res.reason.lower()
