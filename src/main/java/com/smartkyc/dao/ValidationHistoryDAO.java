package com.smartkyc.dao;
import com.smartkyc.model.ValidationRecord;
import java.util.List;
public interface ValidationHistoryDAO {
    List<ValidationRecord> findAll(); List<ValidationRecord> findByFilters(String search,String docType,String status);
    boolean insert(ValidationRecord record); boolean delete(int validationId); boolean clearAll();
    int getTotalValidationsCount(); int getTodayValidationsCount(); int getCountByDocAndStatus(String docType,String status);
    List<ValidationRecord> findRecent(int limit);
}
