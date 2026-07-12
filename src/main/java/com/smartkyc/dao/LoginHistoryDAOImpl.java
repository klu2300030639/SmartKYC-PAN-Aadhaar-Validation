package com.smartkyc.dao;
import com.smartkyc.database.ConnectionFactory;
import com.smartkyc.model.LoginRecord;
import java.sql.*;
import java.util.*;
import java.util.logging.*;
public class LoginHistoryDAOImpl implements LoginHistoryDAO {
    private static final Logger logger=Logger.getLogger(LoginHistoryDAOImpl.class.getName());
    @Override public boolean insert(LoginRecord r){String sql="INSERT INTO login_history(user_id,login_status,ip_address,device_name)VALUES(?,?,?,?)";try(Connection c=ConnectionFactory.getConnection();PreparedStatement ps=c.prepareStatement(sql,Statement.RETURN_GENERATED_KEYS)){if(r.getUserId()>0)ps.setInt(1,r.getUserId());else ps.setNull(1,Types.INTEGER);ps.setString(2,r.getLoginStatus());ps.setString(3,r.getIpAddress());ps.setString(4,r.getDeviceName());if(ps.executeUpdate()>0){try(ResultSet k=ps.getGeneratedKeys()){if(k.next())r.setLoginId(k.getInt(1));}return true;}}catch(SQLException e){logger.log(Level.SEVERE,"insert",e);}return false;}
    @Override public boolean updateLogoutTime(int id){try(Connection c=ConnectionFactory.getConnection();PreparedStatement ps=c.prepareStatement("UPDATE login_history SET logout_time=NOW() WHERE login_id=?")){ps.setInt(1,id);return ps.executeUpdate()>0;}catch(SQLException e){logger.log(Level.SEVERE,"updateLogout",e);}return false;}
    @Override public List<LoginRecord> findRecentAttempts(int limit){List<LoginRecord> l=new ArrayList<>();String sql="SELECT lh.*,u.username FROM login_history lh LEFT JOIN users u ON lh.user_id=u.user_id ORDER BY lh.login_time DESC LIMIT ?";try(Connection c=ConnectionFactory.getConnection();PreparedStatement ps=c.prepareStatement(sql)){ps.setInt(1,limit);try(ResultSet rs=ps.executeQuery()){while(rs.next()){String u=rs.getString("username");if(u==null)u="Unknown";l.add(new LoginRecord(rs.getInt("login_id"),rs.getInt("user_id"),u,rs.getTimestamp("login_time"),rs.getTimestamp("logout_time"),rs.getString("login_status"),rs.getString("ip_address"),rs.getString("device_name")));}}}catch(SQLException e){logger.log(Level.SEVERE,"findRecent",e);}return l;}
}
