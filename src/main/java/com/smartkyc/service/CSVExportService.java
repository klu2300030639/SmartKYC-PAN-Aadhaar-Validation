package com.smartkyc.service;
import com.smartkyc.model.ValidationRecord;
import java.io.*;
import java.util.List;
import java.util.logging.*;
public class CSVExportService {
    private static final Logger logger=Logger.getLogger(CSVExportService.class.getName());
    public static boolean exportValidationHistory(List<ValidationRecord> records,String filePath){
        try(PrintWriter pw=new PrintWriter(new FileWriter(filePath))){
            pw.println("Validation ID,Document Type,Document Number,Status,Reason,Validated At");
            for(ValidationRecord r:records){
                String reason=r.getReason()!=null?r.getReason().replace("\"","'"):"";
                pw.printf("%d,%s,%s,%s,\"%s\",%s%n",r.getValidationId(),r.getDocumentType(),r.getDocumentNumber(),r.getStatus(),reason,r.getValidatedAt());
            }
            AuditService.log("CSV_EXPORT","Validation History","Exported "+records.size()+" records to "+filePath);
            return true;
        }catch(IOException e){logger.log(Level.SEVERE,"CSV export failed",e);return false;}
    }
}
