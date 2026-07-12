package com.smartkyc.controller;
import com.smartkyc.model.ValidationResult;
import com.smartkyc.service.ValidationService;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
public class AadhaarValidationController {
    @FXML private TextField aadhaarInputField;
    @FXML private VBox resultCard;
    @FXML private Label resultStatusLabel,resultAadhaarLabel,resultReasonLabel;
    @FXML public void handleValidate(){
        String input=aadhaarInputField.getText().trim();
        if(input.isEmpty()){resultStatusLabel.setText("Please enter an Aadhaar number.");resultCard.setVisible(true);return;}
        ValidationResult r=ValidationService.validateAadhaar(input);
        resultCard.setVisible(true);resultAadhaarLabel.setText(r.getNormalizedInput());resultReasonLabel.setText(r.getReason());
        resultStatusLabel.setText(r.getStatus());resultStatusLabel.getStyleClass().clear();
        resultStatusLabel.getStyleClass().add(r.isValid()?"badge-valid":"badge-invalid");
    }
    @FXML public void handleClear(){aadhaarInputField.clear();resultCard.setVisible(false);resultStatusLabel.getStyleClass().clear();}
}
