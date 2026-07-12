package com.smartkyc.service;
import com.smartkyc.dao.ValidationHistoryDAO;
import com.smartkyc.dao.ValidationHistoryDAOImpl;
import com.smartkyc.model.ValidationRecord;
import com.smartkyc.model.ValidationResult;
import com.smartkyc.security.SecurityContext;
import com.smartkyc.validator.AadhaarValidator;
import com.smartkyc.validator.PANValidator;
public class ValidationService {
    private static final ValidationHistoryDAO dao=new ValidationHistoryDAOImpl();
    public static ValidationResult validatePAN(String input){
        ValidationResult r=PANValidator.validate(input);
        int uid=SecurityContext.getCurrentUser()!=null?SecurityContext.getCurrentUser().getUserId():0;
        dao.insert(new ValidationRecord(0,uid,r.getDocumentType(),r.getNormalizedInput(),r.getStatus(),r.getReason(),null));
        AuditService.log(r.isValid()?"PAN_VALIDATION":"PAN_VALIDATION_FAILURE","KYC Validation","PAN: "+r.getNormalizedInput()+", Status: "+r.getStatus());
        return r;
    }
    public static ValidationResult validateAadhaar(String input){
        ValidationResult r=AadhaarValidator.validate(input);
        int uid=SecurityContext.getCurrentUser()!=null?SecurityContext.getCurrentUser().getUserId():0;
        dao.insert(new ValidationRecord(0,uid,r.getDocumentType(),r.getNormalizedInput(),r.getStatus(),r.getReason(),null));
        AuditService.log(r.isValid()?"AADHAAR_VALIDATION":"AADHAAR_VALIDATION_FAILURE","KYC Validation","Aadhaar: "+r.getNormalizedInput()+", Status: "+r.getStatus());
        return r;
    }
}
