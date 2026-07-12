package com.smartkyc.model;
import java.sql.Timestamp;
public class AuditLog {
    private int logId,userId; private String username,action,module,description; private Timestamp createdAt;
    public AuditLog(int logId,int userId,String username,String action,String module,String description,Timestamp createdAt){
        this.logId=logId;this.userId=userId;this.username=username;this.action=action;this.module=module;this.description=description;this.createdAt=createdAt;
    }
    public int getLogId(){return logId;} public int getUserId(){return userId;} public String getUsername(){return username;}
    public String getAction(){return action;} public String getModule(){return module;}
    public String getDescription(){return description;} public Timestamp getCreatedAt(){return createdAt;}
}
