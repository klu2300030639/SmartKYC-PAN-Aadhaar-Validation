package com.smartkyc.database;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DatabaseManager {
    private static final Logger logger = Logger.getLogger(DatabaseManager.class.getName());

    public static boolean checkConnection() {
        try (Connection conn = ConnectionFactory.getConnection()) {
            return conn != null && !conn.isClosed();
        } catch (SQLException e) { logger.log(Level.SEVERE, "DB connection check failed", e); return false; }
    }

    public static void initializeDatabase() {
        String[] tables = {"users","validation_history","audit_logs","login_history","application_settings"};
        try (Connection conn = ConnectionFactory.getConnection()) {
            for (String t : tables) {
                if (!tableExists(conn, t)) logger.log(Level.WARNING, "Table missing: " + t);
                else logger.log(Level.INFO, "Table OK: " + t);
            }
        } catch (SQLException e) { logger.log(Level.SEVERE, "Failed to verify schema", e); }
    }

    private static boolean tableExists(Connection conn, String name) throws SQLException {
        try (ResultSet rs = conn.getMetaData().getTables(null, null, name, new String[]{"TABLE"})) { return rs.next(); }
    }
}
