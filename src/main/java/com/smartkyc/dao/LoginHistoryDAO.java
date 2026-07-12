package com.smartkyc.dao;
import com.smartkyc.model.LoginRecord;
import java.util.List;
public interface LoginHistoryDAO {
    boolean insert(LoginRecord record); boolean updateLogoutTime(int loginId); List<LoginRecord> findRecentAttempts(int limit);
}
