import re

class ValidationResult:
    def __init__(self, valid: bool, reason: str, document_type: str, normalized_input: str):
        self.valid = valid
        self.reason = reason
        self.document_type = document_type
        self.normalized_input = normalized_input

# Verhoeff Tables
d = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

p = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

def verhoeff_validate(number: str) -> bool:
    try:
        c = 0
        digits = [int(x) for x in number]
        length = len(digits)
        for i in range(length):
            index = (length - i) % 8
            digit = digits[i]
            c = d[c][p[index][digit]]
        return c == 0
    except Exception:
        return False

def normalize_input(raw_input: str) -> str:
    if raw_input is None:
        return ""
    return str(raw_input).strip().upper()

def validate_pan(raw_input: str) -> ValidationResult:
    n = normalize_input(raw_input)
    if not n:
        return ValidationResult(False, "PAN cannot be empty", "PAN", n)
    if len(n) != 10:
        return ValidationResult(False, "PAN must be exactly 10 characters", "PAN", n)
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", n):
        return ValidationResult(False, "PAN format invalid. Expected: 5 letters + 4 digits + 1 letter (e.g. ABCDE1234F)", "PAN", n)
    
    valid_cats = {'P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G'}
    cat = n[3]
    if cat not in valid_cats:
        return ValidationResult(False, f"Invalid 4th character '{cat}'. Valid: P, C, H, F, A, T, B, L, J, G", "PAN", n)
        
    return ValidationResult(True, "Valid PAN format and category verified.", "PAN", n)

def validate_aadhaar(raw_input: str) -> ValidationResult:
    n = normalize_input(raw_input)
    if not n:
        return ValidationResult(False, "Aadhaar number cannot be empty", "Aadhaar", n)
    if not n.isdigit():
        return ValidationResult(False, "Must contain digits only", "Aadhaar", n)
    if len(n) != 12:
        return ValidationResult(False, "Must be exactly 12 digits", "Aadhaar", n)
    if int(n[0]) < 2:
        return ValidationResult(False, "First digit cannot be 0 or 1", "Aadhaar", n)
    if not verhoeff_validate(n):
        return ValidationResult(False, "Invalid Verhoeff checksum — number does not exist", "Aadhaar", n)
        
    return ValidationResult(True, "Valid Aadhaar format and checksum verified.", "Aadhaar", n)
