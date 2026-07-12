package com.smartkyc.model;
import java.sql.Timestamp;
public class User {
    private int userId; private String fullName, username, email, passwordHash, phone, role, status;
    private Timestamp createdAt, updatedAt;
    public User(int userId,String fullName,String username,String email,String passwordHash,String phone,String role,String status,Timestamp createdAt,Timestamp updatedAt){
        this.userId=userId;this.fullName=fullName;this.username=username;this.email=email;this.passwordHash=passwordHash;this.phone=phone;this.role=role;this.status=status;this.createdAt=createdAt;this.updatedAt=updatedAt;
    }
    public int getUserId(){return userId;} public void setUserId(int v){userId=v;}
    public String getFullName(){return fullName;} public void setFullName(String v){fullName=v;}
    public String getUsername(){return username;} public void setUsername(String v){username=v;}
    public String getEmail(){return email;} public void setEmail(String v){email=v;}
    public String getPasswordHash(){return passwordHash;} public void setPasswordHash(String v){passwordHash=v;}
    public String getPhone(){return phone;} public void setPhone(String v){phone=v;}
    public String getRole(){return role;} public void setRole(String v){role=v;}
    public String getStatus(){return status;} public void setStatus(String v){status=v;}
    public Timestamp getCreatedAt(){return createdAt;} public Timestamp getUpdatedAt(){return updatedAt;}
}
