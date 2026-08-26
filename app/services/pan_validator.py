"""
PAN (Permanent Account Number) Validation Service.
Matches the official Income Tax Department 10-character alphanumeric structure.
"""
import re

PAN_REGEX = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

# 4th character entity mapping (Income Tax Department Category)
PAN_ENTITIES = {
    'A': 'Association of Persons (AOP)',
    'B': 'Body of Individuals (BOI)',
    'C': 'Company',
    'F': 'Firm / Limited Liability Partnership (LLP)',
    'G': 'Government Agency',
    'H': 'Hindu Undivided Family (HUF)',
    'L': 'Local Authority',
    'J': 'Artificial Juridical Person',
    'P': 'Individual / Person',
    'T': 'Trust'
}


def validate_pan(pan_number: str) -> dict:
    """
    Validates a PAN number:
    - 10 alphanumeric uppercase characters
    - Pattern: [A-Z]{5}[0-9]{4}[A-Z]{1}
    - 4th character determines the category holder
    - 5th character matches the first character of holder's surname
    """
    if not pan_number:
        return {"valid": False, "reason": "PAN number cannot be empty."}
        
    clean_pan = pan_number.strip().upper()
    
    if len(clean_pan) != 10:
        return {
            "valid": False,
            "reason": f"PAN must be exactly 10 characters (Received {len(clean_pan)})."
        }
        
    if not re.match(PAN_REGEX, clean_pan):
        return {
            "valid": False,
            "reason": "Invalid PAN format. Must follow standard pattern (e.g. ABCDE1234F)."
        }
        
    entity_code = clean_pan[3]
    entity_type = PAN_ENTITIES.get(entity_code, "Special / Custom Jurisdiction Entity")
    surname_initial = clean_pan[4]
    
    return {
        "valid": True,
        "reason": "PAN format is structurally valid.",
        "pan": clean_pan,
        "entity_code": entity_code,
        "entity_type": entity_type,
        "surname_initial": surname_initial
    }
