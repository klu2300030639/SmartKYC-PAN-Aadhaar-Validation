package com.smartkyc.model;
public class ValidationResult {
    private final boolean valid; private final String reason,documentType,normalizedInput;
    public ValidationResult(boolean valid,String reason,String documentType,String normalizedInput){
        this.valid=valid;this.reason=reason;this.documentType=documentType;this.normalizedInput=normalizedInput;
    }
    public boolean isValid(){return valid;} public String getReason(){return reason;}
    public String getDocumentType(){return documentType;} public String getNormalizedInput(){return normalizedInput;}
    public String getStatus(){return valid?"Valid":"Invalid";}
}
