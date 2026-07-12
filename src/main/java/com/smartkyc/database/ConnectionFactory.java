package com.smartkyc.database;

import com.smartkyc.config.ConfigurationManager;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ConnectionFactory {
    private static final Logger logger = Logger.getLogger(ConnectionFactory.class.getName());
    static {
        try { Class.forName("com.mysql.cj.jdbc.Driver"); }
        catch (ClassNotFoundException e) { logger.log(Level.SEVERE, "MySQL JDBC Driver not found!", e); }
    }
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(ConfigurationManager.getDbUrl(), ConfigurationManager.getDbUsername(), ConfigurationManager.getDbPassword());
    }
}
