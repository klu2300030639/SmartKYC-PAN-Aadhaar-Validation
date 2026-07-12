package com.smartkyc.service;
import com.smartkyc.dao.ValidationHistoryDAO;
import com.smartkyc.dao.ValidationHistoryDAOImpl;
import com.smartkyc.model.ValidationRecord;
import java.util.List;
public class HistoryService {
    private static final ValidationHistoryDAO dao=new ValidationHistoryDAOImpl();
    public static List<ValidationRecord> getHistory(){return dao.findAll();}
    public static List<ValidationRecord> getHistoryByFilters(String s,String d,String st){return dao.findByFilters(s,d,st);}
    public static boolean deleteRecord(int id){boolean ok=dao.delete(id);if(ok)AuditService.log("RECORD_DELETION","Validation History","Deleted record ID: "+id);return ok;}
    public static boolean clearHistory(){boolean ok=dao.clearAll();if(ok)AuditService.log("CLEAR_HISTORY","Settings","Cleared all KYC validation history.");return ok;}
    public static int getTotalCount(){return dao.getTotalValidationsCount();}
    public static int getTodayCount(){return dao.getTodayValidationsCount();}
    public static int getCount(String dt,String st){return dao.getCountByDocAndStatus(dt,st);}
    public static List<ValidationRecord> getRecentValidations(int limit){return dao.findRecent(limit);}
}
