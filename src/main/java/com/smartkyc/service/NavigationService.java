package com.smartkyc.service;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.layout.StackPane;
import java.io.IOException;
import java.util.logging.*;
public class NavigationService {
    private static final Logger logger=Logger.getLogger(NavigationService.class.getName());
    private static StackPane contentPane;
    public static void setContentPane(StackPane p){contentPane=p;}
    public static void navigateTo(String fxml){
        if(contentPane==null){logger.log(Level.SEVERE,"ContentPane not set!");return;}
        try{FXMLLoader loader=new FXMLLoader(NavigationService.class.getResource("/view/"+fxml));Parent view=loader.load();contentPane.getChildren().setAll(view);}
        catch(IOException e){logger.log(Level.SEVERE,"Navigation failed: "+fxml,e);}
    }
}
