"""
Verhoeff Algorithm for Aadhaar (UIDAI) 12-Digit Offline Checksum Validation.
Uses Dihedral Group D5 multiplication, permutation, and inverse matrices.
"""

# The multiplication table (d)
D_TABLE = [
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

# The permutation table (p)
P_TABLE = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

# The inverse table (inv)
INV_TABLE = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def validate_verhoeff(num_str: str) -> bool:
    """
    Validates a number string using the Verhoeff Dihedral Group D5 algorithm.
    Returns True if valid, False otherwise.
    """
    if not num_str or not num_str.isdigit():
        return False
    
    try:
        c = 0
        digits = [int(x) for x in num_str]
        length = len(digits)
        for i in range(length):
            index = (length - i) % 8
            digit = digits[i]
            c = D_TABLE[c][P_TABLE[index][digit]]
        return c == 0
    except Exception:
        return False



def validate_aadhaar(aadhaar_num: str) -> dict:
    """
    Validates an Aadhaar card number:
    - 12 digits length
    - Numeric characters only
    - Cannot start with 0 or 1 (UIDAI specifications)
    - Verhoeff checksum algorithm validation
    """
    if not aadhaar_num:
        return {"valid": False, "reason": "Aadhaar number cannot be empty."}
    
    clean_num = aadhaar_num.replace(" ", "").replace("-", "").strip()
    
    if len(clean_num) != 12:
        return {
            "valid": False,
            "reason": f"Aadhaar must be exactly 12 digits (Received {len(clean_num)} digits)."
        }
        
    if not clean_num.isdigit():
        return {"valid": False, "reason": "Aadhaar must contain only numeric digits."}
        
    if clean_num[0] in ('0', '1'):
        return {"valid": False, "reason": "Invalid Aadhaar: Cannot start with 0 or 1."}
        
    if not validate_verhoeff(clean_num):
        return {"valid": False, "reason": "Invalid Aadhaar: Failed Verhoeff algorithmic checksum."}
        
    formatted = f"{clean_num[:4]} {clean_num[4:8]} {clean_num[8:]}"
    return {
        "valid": True,
        "reason": "Aadhaar number is structurally and algorithmically valid (Verhoeff checksum passed).",
        "formatted": formatted,
        "raw": clean_num
    }
