package com.smartkyc.controller;
import com.smartkyc.config.ConfigurationManager;
import com.smartkyc.dao.SettingsDAO;
import com.smartkyc.dao.SettingsDAOImpl;
import com.smartkyc.database.DatabaseManager;
import com.smartkyc.security.SecurityContext;
import com.smartkyc.service.*;
import javafx.fxml.FXML;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
public class SettingsController {
    @FXML private RadioButton darkThemeRadio,lightThemeRadio;
    @FXML private TextField dbUrlField,dbUserField;
    @FXML private Label connectionStatusLabel;
    @FXML private VBox adminActionsCard;
    private final SettingsDAO settingsDAO=new SettingsDAOImpl();
    @FXML public void initialize(){
        ToggleGroup tg=new ToggleGroup();darkThemeRadio.setToggleGroup(tg);lightThemeRadio.setToggleGroup(tg);
        String theme=settingsDAO.get("theme");
        if("dark".equalsIgnoreCase(theme))darkThemeRadio.setSelected(true);else lightThemeRadio.setSelected(true);
        dbUrlField.setText(ConfigurationManager.getDbUrl());dbUserField.setText(ConfigurationManager.getDbUsername());
        boolean admin=SecurityContext.isAdmin();adminActionsCard.setVisible(admin);adminActionsCard.setManaged(admin);
    }
    @FXML private void handleApplyTheme(){
        String t=darkThemeRadio.isSelected()?"dark":"light";
        if(settingsDAO.set("theme",t)){
            Scene scene=darkThemeRadio.getScene();
            if(scene!=null){Parent root=scene.getRoot();if("dark".equals(t)){if(!root.getStyleClass().contains("dark-theme"))root.getStyleClass().add("dark-theme");}else root.getStyleClass().remove("dark-theme");}
            AlertService.showInfo("Theme","Applied","Theme changed to "+t.toUpperCase()+" mode.");
        }else AlertService.showError("Error","Failed","Could not save theme preference.");
    }
    @FXML private void handleTestConnection(){
        connectionStatusLabel.setText("Testing...");
        boolean ok=DatabaseManager.checkConnection();
        connectionStatusLabel.setText(ok?"● Connected":"● Connection Failed");
        connectionStatusLabel.setStyle(ok?"-fx-text-fill:#10b981;-fx-font-weight:bold;":"-fx-text-fill:#ef4444;-fx-font-weight:bold;");
    }
    @FXML private void handleClearHistory(){if(AlertService.showConfirmation("Clear","Confirm","Permanently delete all validation history? Cannot be undone.")){if(HistoryService.clearHistory())AlertService.showInfo("Done","Cleared","All validation history removed.");else AlertService.showError("Error","Failed","Could not clear history.");}}
    @FXML private void handleClearLogs(){if(AlertService.showConfirmation("Clear","Confirm","Permanently clear all audit logs? Cannot be undone.")){if(AuditService.clearLogs())AlertService.showInfo("Done","Cleared","All audit logs removed.");else AlertService.showError("Error","Failed","Could not clear logs.");}}
}
