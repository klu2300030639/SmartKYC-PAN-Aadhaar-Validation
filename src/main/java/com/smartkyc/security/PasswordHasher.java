package com.smartkyc.security;
import org.mindrot.jbcrypt.BCrypt;
public class PasswordHasher {
    public static String hash(String plain){ return BCrypt.hashpw(plain, BCrypt.gensalt(10)); }
    public static boolean check(String plain,String hashed){
        if(hashed==null||!hashed.startsWith("$2a$"))return false;
        return BCrypt.checkpw(plain,hashed);
    }
}
