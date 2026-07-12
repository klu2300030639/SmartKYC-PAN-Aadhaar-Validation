package com.smartkyc.controller;
import com.smartkyc.dao.SettingsDAO;
import com.smartkyc.dao.SettingsDAOImpl;
import com.smartkyc.service.AuthenticationService;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.stage.Stage;
import java.io.IOException;
public class LoginController {
    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Label errorLabel;
    @FXML public void handleLogin(ActionEvent event){
        String u=usernameField.getText().trim(),p=passwordField.getText();
        if(u.isEmpty()||p.isEmpty()){errorLabel.setText("Please enter both username and password.");return;}
        if(AuthenticationService.login(u,p)){
            try{
                FXMLLoader loader=new FXMLLoader(getClass().getResource("/view/main_layout.fxml"));
                Parent root=loader.load();
                SettingsDAO sd=new SettingsDAOImpl();
                String theme=sd.get("theme");
                if("dark".equalsIgnoreCase(theme))root.getStyleClass().add("dark-theme");
                Stage stage=(Stage)((Node)event.getSource()).getScene().getWindow();
                Scene scene=new Scene(root,1200,780);
                stage.setScene(scene);stage.setTitle("SmartKYC - PAN & Aadhaar Validation System");
                stage.setResizable(true);stage.setMaximized(true);stage.show();
            }catch(IOException e){errorLabel.setText("Error loading workspace: "+e.getMessage());}
        }else{errorLabel.setText("Invalid credentials or account inactive.");}
    }
}
