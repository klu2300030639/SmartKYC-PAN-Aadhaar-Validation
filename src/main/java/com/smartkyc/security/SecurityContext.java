package com.smartkyc.security;
import com.smartkyc.model.User;
public class SecurityContext {
    private static User currentUser; private static int currentLoginId;
    public static void setCurrentUser(User u){currentUser=u;}
    public static User getCurrentUser(){return currentUser;}
    public static boolean isLoggedIn(){return currentUser!=null;}
    public static boolean isAdmin(){return currentUser!=null&&"Admin".equalsIgnoreCase(currentUser.getRole());}
    public static void setCurrentLoginId(int id){currentLoginId=id;}
    public static int getCurrentLoginId(){return currentLoginId;}
    public static void clear(){currentUser=null;currentLoginId=0;}
}
