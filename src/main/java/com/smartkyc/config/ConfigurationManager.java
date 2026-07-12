package com.smartkyc.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ConfigurationManager {
    private static final Logger logger = Logger.getLogger(ConfigurationManager.class.getName());
    private static final Properties properties = new Properties();

    static {
        try (InputStream input = ConfigurationManager.class.getClassLoader().getResourceAsStream("config.properties")) {
            if (input == null) logger.log(Level.SEVERE, "Unable to find config.properties");
            else { properties.load(input); logger.log(Level.INFO, "Configuration loaded."); }
        } catch (IOException ex) { logger.log(Level.SEVERE, "Error loading config", ex); }
    }

    public static String getProperty(String key, String defaultValue) { return properties.getProperty(key, defaultValue); }
    public static String getDbUrl() { return getProperty("db.url", "jdbc:mysql://localhost:3306/KYCValidatorDB"); }
    public static String getDbUsername() { return getProperty("db.username", "root"); }
    public static String getDbPassword() { return getProperty("db.password", "root"); }
    public static String getAppName() { return getProperty("app.name", "SmartKYC"); }
    public static String getAppVersion() { return getProperty("app.version", "1.0.0"); }
    public static String getAppTheme() { return getProperty("app.theme", "dark"); }
    public static String getLogPath() { return getProperty("app.log.path", "logs/application.log"); }
}
