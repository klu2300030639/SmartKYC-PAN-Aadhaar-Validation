package com.smartkyc.dao;
import com.smartkyc.model.AuditLog;
import java.util.List;
public interface AuditLogDAO {
    boolean insert(AuditLog log); List<AuditLog> findAll();
    List<AuditLog> findByFilters(String search,String module,String action);
    boolean clearAll(); List<AuditLog> findRecent(int limit);
}
