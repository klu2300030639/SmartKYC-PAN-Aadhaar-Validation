package com.smartkyc.controller;
import com.smartkyc.database.DatabaseManager;
import com.smartkyc.security.SecurityContext;
import com.smartkyc.service.AuthenticationService;
import com.smartkyc.service.NavigationService;
import com.smartkyc.utils.DateUtil;
import javafx.animation.*;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import javafx.util.Duration;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.logging.*;
public class MainController {
    private static final Logger logger=Logger.getLogger(MainController.class.getName());
    @FXML private Button dashboardBtn,validatePanBtn,validateAadhaarBtn,historyBtn,logsBtn,usersBtn,settingsBtn,aboutBtn;
    @FXML private Label titleLabel,userLabel,dbStatusLabel,timeLabel;
    @FXML private StackPane contentPane;
    private Button activeBtn;
    @FXML public void initialize(){
        NavigationService.setContentPane(contentPane);
        if(SecurityContext.isLoggedIn()){
            var user=SecurityContext.getCurrentUser();
            userLabel.setText("Welcome, "+user.getFullName()+" ("+user.getRole()+")");
            boolean admin=SecurityContext.isAdmin();
            logsBtn.setVisible(admin);logsBtn.setManaged(admin);
            usersBtn.setVisible(admin);usersBtn.setManaged(admin);
        }else{userLabel.setText("Welcome, Guest");logsBtn.setVisible(false);logsBtn.setManaged(false);usersBtn.setVisible(false);usersBtn.setManaged(false);}
        boolean db=DatabaseManager.checkConnection();
        dbStatusLabel.setText(db?"● DB: Connected":"● DB: Offline");
        dbStatusLabel.setStyle(db?"-fx-text-fill:#00e676;-fx-font-weight:bold;":"-fx-text-fill:#ff5252;-fx-font-weight:bold;");
        Timeline clock=new Timeline(new KeyFrame(Duration.ZERO,e->timeLabel.setText(DateUtil.formatDateTime(new Timestamp(System.currentTimeMillis())))),new KeyFrame(Duration.seconds(1)));
        clock.setCycleCount(Animation.INDEFINITE);clock.play();
        activeBtn=dashboardBtn;showDashboard();
    }
    private void setActive(Button btn,String title){if(activeBtn!=null)activeBtn.getStyleClass().remove("nav-btn-active");btn.getStyleClass().add("nav-btn-active");activeBtn=btn;titleLabel.setText(title);}
    @FXML public void showDashboard(){setActive(dashboardBtn,"Dashboard Overview");NavigationService.navigateTo("dashboard.fxml");}
    @FXML public void showValidatePAN(){setActive(validatePanBtn,"Validate PAN Card");NavigationService.navigateTo("pan_validation.fxml");}
    @FXML public void showValidateAadhaar(){setActive(validateAadhaarBtn,"Validate Aadhaar");NavigationService.navigateTo("aadhaar_validation.fxml");}
    @FXML public void showHistory(){setActive(historyBtn,"KYC Validation History");NavigationService.navigateTo("validation_history.fxml");}
    @FXML public void showLogs(){setActive(logsBtn,"System Audit Logs");NavigationService.navigateTo("audit_logs.fxml");}
    @FXML public void showUsers(){setActive(usersBtn,"User Management");NavigationService.navigateTo("user_management.fxml");}
    @FXML public void showSettings(){setActive(settingsBtn,"Application Settings");NavigationService.navigateTo("settings.fxml");}
    @FXML public void showAbout(){setActive(aboutBtn,"About SmartKYC");NavigationService.navigateTo("about.fxml");}
    @FXML public void handleSignOut(ActionEvent event){
        AuthenticationService.logout();
        try{FXMLLoader loader=new FXMLLoader(getClass().getResource("/view/login.fxml"));Parent root=loader.load();
            Stage stage=(Stage)((Node)event.getSource()).getScene().getWindow();
            stage.setScene(new Scene(root,450,580));stage.setTitle("SmartKYC - Sign In");stage.setMaximized(false);stage.setResizable(false);stage.centerOnScreen();stage.show();
        }catch(IOException e){logger.log(Level.SEVERE,"Failed to load login",e);}
    }
}
