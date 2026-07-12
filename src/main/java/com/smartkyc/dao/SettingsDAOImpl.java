package com.smartkyc.dao;
import com.smartkyc.database.ConnectionFactory;
import java.sql.*;
import java.util.*;
import java.util.logging.*;
public class SettingsDAOImpl implements SettingsDAO {
    private static final Logger logger=Logger.getLogger(SettingsDAOImpl.class.getName());
    @Override public String get(String key){try(Connection c=ConnectionFactory.getConnection();PreparedStatement ps=c.prepareStatement("SELECT setting_value FROM application_settings WHERE setting_key=?")){ps.setString(1,key);try(ResultSet rs=ps.executeQuery()){if(rs.next())return rs.getString("setting_value");}}catch(SQLException e){logger.log(Level.SEVERE,"get "+key,e);}return null;}
    @Override public boolean set(String key,String value){String sql="INSERT INTO application_settings(setting_key,setting_value)VALUES(?,?) ON DUPLICATE KEY UPDATE setting_value=?";try(Connection c=ConnectionFactory.getConnection();PreparedStatement ps=c.prepareStatement(sql)){ps.setString(1,key);ps.setString(2,value);ps.setString(3,value);return ps.executeUpdate()>0;}catch(SQLException e){logger.log(Level.SEVERE,"set "+key,e);}return false;}
    @Override public Map<String,String> getAll(){Map<String,String> map=new HashMap<>();try(Connection c=ConnectionFactory.getConnection();Statement s=c.createStatement();ResultSet rs=s.executeQuery("SELECT * FROM application_settings")){while(rs.next())map.put(rs.getString("setting_key"),rs.getString("setting_value"));}catch(SQLException e){logger.log(Level.SEVERE,"getAll",e);}return map;}
}
