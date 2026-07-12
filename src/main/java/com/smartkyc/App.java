package com.smartkyc;

import com.smartkyc.dao.SettingsDAO;
import com.smartkyc.dao.SettingsDAOImpl;
import com.smartkyc.database.DatabaseManager;
import com.smartkyc.service.LoggingService;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class App extends Application {
    private static final Logger logger = Logger.getLogger(App.class.getName());

    @Override
    public void start(Stage primaryStage) {
        LoggingService.initialize();
        logger.info("Starting SmartKYC application...");
        DatabaseManager.initializeDatabase();
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/view/login.fxml"));
            Parent root = loader.load();
            Scene scene = new Scene(root, 450, 580);
            try {
                var cssResource = getClass().getResource("/css/style.css");
                if (cssResource != null) scene.getStylesheets().add(cssResource.toExternalForm());
                SettingsDAO settingsDAO = new SettingsDAOImpl();
                String theme = settingsDAO.get("theme");
                if ("dark".equalsIgnoreCase(theme)) root.getStyleClass().add("dark-theme");
            } catch (Exception e) {
                logger.log(Level.WARNING, "Failed to apply styles on startup", e);
            }
            primaryStage.setScene(scene);
            primaryStage.setTitle("SmartKYC - Sign In");
            primaryStage.setResizable(false);
            primaryStage.centerOnScreen();
            primaryStage.setOnCloseRequest(ev -> { logger.info("Shutting down SmartKYC..."); LoggingService.close(); });
            primaryStage.show();
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Failed to load FXML", e);
        }
    }

    public static void main(String[] args) { launch(args); }
}
