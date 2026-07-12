package com.smartkyc.service;
import com.smartkyc.dao.UserDAO;
import com.smartkyc.dao.UserDAOImpl;
import com.smartkyc.model.User;
import com.smartkyc.security.PasswordHasher;
public class RegistrationService {
    private static final UserDAO userDAO=new UserDAOImpl();
    public static boolean register(String fullName,String username,String email,String password,String phone,String role){
        if(userDAO.findByUsername(username)!=null)return false;
        String hash=PasswordHasher.hash(password);
        User u=new User(0,fullName,username,email,hash,phone,role,"Active",null,null);
        boolean ok=userDAO.insert(u);
        if(ok)AuditService.log("USER_CREATE","User Management","Created user: "+username+" role: "+role);
        return ok;
    }
}
