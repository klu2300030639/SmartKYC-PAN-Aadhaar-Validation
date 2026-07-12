package com.smartkyc.controller;
import com.smartkyc.model.ValidationResult;
import com.smartkyc.service.ValidationService;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
public class PANValidationController {
    @FXML private TextField panInputField;
    @FXML private VBox resultCard;
    @FXML private Label resultStatusLabel,resultPanLabel,resultReasonLabel;
    @FXML public void handleValidate(){
        String input=panInputField.getText().trim();
        if(input.isEmpty()){resultStatusLabel.setText("Please enter a PAN number.");resultCard.setVisible(true);return;}
        ValidationResult r=ValidationService.validatePAN(input);
        resultCard.setVisible(true);resultPanLabel.setText(r.getNormalizedInput());resultReasonLabel.setText(r.getReason());
        resultStatusLabel.setText(r.getStatus());resultStatusLabel.getStyleClass().clear();
        resultStatusLabel.getStyleClass().add(r.isValid()?"badge-valid":"badge-invalid");
    }
    @FXML public void handleClear(){panInputField.clear();resultCard.setVisible(false);resultStatusLabel.getStyleClass().clear();}
}
