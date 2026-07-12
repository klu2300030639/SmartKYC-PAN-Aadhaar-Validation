package com.smartkyc.model;
import java.sql.Timestamp;
public class ValidationRecord {
    private int validationId,userId; private String documentType,documentNumber,status,reason; private Timestamp validatedAt;
    public ValidationRecord(int validationId,int userId,String documentType,String documentNumber,String status,String reason,Timestamp validatedAt){
        this.validationId=validationId;this.userId=userId;this.documentType=documentType;this.documentNumber=documentNumber;this.status=status;this.reason=reason;this.validatedAt=validatedAt;
    }
    public int getValidationId(){return validationId;} public int getUserId(){return userId;}
    public String getDocumentType(){return documentType;} public String getDocumentNumber(){return documentNumber;}
    public String getStatus(){return status;} public String getReason(){return reason;} public Timestamp getValidatedAt(){return validatedAt;}
}
