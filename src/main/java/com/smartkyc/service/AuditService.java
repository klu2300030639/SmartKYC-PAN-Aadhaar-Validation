package com.smartkyc.service;
import com.smartkyc.dao.AuditLogDAO;
import com.smartkyc.dao.AuditLogDAOImpl;
import com.smartkyc.model.AuditLog;
import com.smartkyc.security.SecurityContext;
import java.util.List;
import java.util.logging.Logger;
public class AuditService {
    private static final Logger logger=Logger.getLogger(AuditService.class.getName());
    private static final AuditLogDAO dao=new AuditLogDAOImpl();
    public static void log(String action,String module,String description){
        int uid=SecurityContext.getCurrentUser()!=null?SecurityContext.getCurrentUser().getUserId():0;
        String uname=SecurityContext.getCurrentUser()!=null?SecurityContext.getCurrentUser().getUsername():"SYSTEM";
        logger.info(String.format("AUDIT: user=%s module=%s action=%s details=%s",uname,module,action,description));
        dao.insert(new AuditLog(0,uid,uname,action,module,description,null));
    }
    public static List<AuditLog> getLogs(){return dao.findAll();}
    public static List<AuditLog> getLogsByFilters(String s,String m,String a){return dao.findByFilters(s,m,a);}
    public static boolean clearLogs(){boolean ok=dao.clearAll();if(ok)log("CLEAR_LOGS","Settings","Cleared all audit logs.");return ok;}
    public static List<AuditLog> getRecentLogs(int limit){return dao.findRecent(limit);}
}
