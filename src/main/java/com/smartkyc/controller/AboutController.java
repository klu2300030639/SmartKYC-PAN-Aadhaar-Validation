package com.smartkyc.controller;
import com.smartkyc.config.ConfigurationManager;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
public class AboutController {
    @FXML private Label versionLabel,javaVersionLabel;
    @FXML public void initialize(){
        versionLabel.setText(ConfigurationManager.getAppVersion());
        javaVersionLabel.setText(System.getProperty("java.version"));
    }
}
