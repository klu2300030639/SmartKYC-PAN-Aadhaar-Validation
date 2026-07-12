package com.smartkyc.service;
import javafx.scene.control.*;
import javafx.stage.Stage;
import java.util.Optional;
public class AlertService {
    public static void showInfo(String title,String header,String content){show(Alert.AlertType.INFORMATION,title,header,content);}
    public static void showError(String title,String header,String content){show(Alert.AlertType.ERROR,title,header,content);}
    public static void showWarning(String title,String header,String content){show(Alert.AlertType.WARNING,title,header,content);}
    public static boolean showConfirmation(String title,String header,String content){Alert a=new Alert(Alert.AlertType.CONFIRMATION);a.setTitle(title);a.setHeaderText(header);a.setContentText(content);style(a);Optional<ButtonType> r=a.showAndWait();return r.isPresent()&&r.get()==ButtonType.OK;}
    private static void show(Alert.AlertType type,String title,String header,String content){Alert a=new Alert(type);a.setTitle(title);a.setHeaderText(header);a.setContentText(content);style(a);a.showAndWait();}
    private static void style(Alert a){try{var css=AlertService.class.getResource("/css/style.css");if(css!=null)a.getDialogPane().getStylesheets().add(css.toExternalForm());}catch(Exception ignored){}}
}
