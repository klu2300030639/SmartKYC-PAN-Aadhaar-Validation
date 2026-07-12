package com.smartkyc.model;
import java.sql.Timestamp;
public class LoginRecord {
    private int loginId,userId; private String username,loginStatus,ipAddress,deviceName; private Timestamp loginTime,logoutTime;
    public LoginRecord(int loginId,int userId,String username,Timestamp loginTime,Timestamp logoutTime,String loginStatus,String ipAddress,String deviceName){
        this.loginId=loginId;this.userId=userId;this.username=username;this.loginTime=loginTime;this.logoutTime=logoutTime;this.loginStatus=loginStatus;this.ipAddress=ipAddress;this.deviceName=deviceName;
    }
    public int getLoginId(){return loginId;} public void setLoginId(int v){loginId=v;}
    public int getUserId(){return userId;} public String getUsername(){return username;}
    public Timestamp getLoginTime(){return loginTime;} public Timestamp getLogoutTime(){return logoutTime;}
    public String getLoginStatus(){return loginStatus;} public String getIpAddress(){return ipAddress;} public String getDeviceName(){return deviceName;}
}
