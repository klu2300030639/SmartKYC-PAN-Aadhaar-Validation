package com.smartkyc.validator;
import com.smartkyc.model.ValidationResult;
public class AadhaarValidator {
    public static ValidationResult validate(String rawInput){
        String n=InputNormalizer.normalize(rawInput);
        if(n.isEmpty()) return new ValidationResult(false,"Aadhaar number cannot be empty","Aadhaar",n);
        if(!n.matches("\\d+")) return new ValidationResult(false,"Must contain digits only","Aadhaar",n);
        if(n.length()!=12) return new ValidationResult(false,"Must be exactly 12 digits","Aadhaar",n);
        if(n.charAt(0)<'2') return new ValidationResult(false,"First digit cannot be 0 or 1","Aadhaar",n);
        if(!VerhoeffValidator.validate(n)) return new ValidationResult(false,"Invalid Verhoeff checksum — number does not exist","Aadhaar",n);
        return new ValidationResult(true,"Valid Aadhaar format and checksum verified. Note: format/checksum validation only, existence not verified.","Aadhaar",n);
    }
}
