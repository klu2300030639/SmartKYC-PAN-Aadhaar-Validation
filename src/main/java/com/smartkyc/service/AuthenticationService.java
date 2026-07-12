package com.smartkyc.service;
import com.smartkyc.dao.LoginHistoryDAO;
import com.smartkyc.dao.LoginHistoryDAOImpl;
import com.smartkyc.dao.UserDAO;
import com.smartkyc.dao.UserDAOImpl;
import com.smartkyc.model.LoginRecord;
import com.smartkyc.model.User;
import com.smartkyc.security.PasswordHasher;
import com.smartkyc.security.SecurityContext;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.List;
public class AuthenticationService {
    private static final UserDAO userDAO=new UserDAOImpl();
    private static final LoginHistoryDAO loginDAO=new LoginHistoryDAOImpl();
    public static boolean login(String username,String password){
        User user=userDAO.findByUsername(username);
        String ip="127.0.0.1",device="Unknown";
        try{InetAddress h=InetAddress.getLocalHost();ip=h.getHostAddress();device=h.getHostName();}catch(UnknownHostException ignored){}
        if(user!=null&&"Active".equalsIgnoreCase(user.getStatus())&&PasswordHasher.check(password,user.getPasswordHash())){
            SecurityContext.setCurrentUser(user);
            LoginRecord r=new LoginRecord(0,user.getUserId(),user.getUsername(),null,null,"Success",ip,device);
            loginDAO.insert(r);SecurityContext.setCurrentLoginId(r.getLoginId());
            AuditService.log("LOGIN_SUCCESS","Authentication","Logged in from "+ip+" ("+device+")");
            return true;
        }
        int fid=user!=null?user.getUserId():0;
        loginDAO.insert(new LoginRecord(0,fid,username,null,null,"Failed",ip,device));
        AuditService.log("LOGIN_FAILURE","Authentication","Failed login for: "+username+" from "+ip);
        return false;
    }
    public static void logout(){
        if(SecurityContext.isLoggedIn()){
            loginDAO.updateLogoutTime(SecurityContext.getCurrentLoginId());
            AuditService.log("LOGOUT","Authentication","Logged out: "+SecurityContext.getCurrentUser().getUsername());
            SecurityContext.clear();
        }
    }
    public static List<LoginRecord> getRecentLoginAttempts(int limit){return loginDAO.findRecentAttempts(limit);}
}
