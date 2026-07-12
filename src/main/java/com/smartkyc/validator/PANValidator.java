package com.smartkyc.validator;
import com.smartkyc.model.ValidationResult;
import java.util.Set;
import java.util.regex.Pattern;
public class PANValidator {
    private static final Set<Character> VALID_CATS=Set.of('P','C','H','F','A','T','B','L','J','G');
    private static final Pattern PAN=Pattern.compile("[A-Z]{5}[0-9]{4}[A-Z]");
    public static ValidationResult validate(String rawInput){
        String n=InputNormalizer.normalize(rawInput);
        if(n.isEmpty()) return new ValidationResult(false,"PAN cannot be empty","PAN",n);
        if(n.length()!=10) return new ValidationResult(false,"PAN must be exactly 10 characters","PAN",n);
        if(!PAN.matcher(n).matches()) return new ValidationResult(false,"PAN format invalid. Expected: 5 letters + 4 digits + 1 letter (e.g. ABCDE1234F)","PAN",n);
        char cat=n.charAt(3);
        if(!VALID_CATS.contains(cat)) return new ValidationResult(false,"Invalid 4th character '"+cat+"'. Valid: P,C,H,F,A,T,B,L,J,G","PAN",n);
        return new ValidationResult(true,"Valid PAN format and category verified. Note: format/category validation only, existence not verified.","PAN",n);
    }
}
