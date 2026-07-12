package com.smartkyc.controller;
import com.smartkyc.model.AuditLog;
import com.smartkyc.service.AuditService;
import com.smartkyc.utils.DateUtil;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import java.util.List;
public class AuditLogsController {
    @FXML private TextField searchField;
    @FXML private ComboBox<String> moduleFilter,actionFilter;
    @FXML private TableView<AuditLog> logsTable;
    @FXML private TableColumn<AuditLog,String> userCol,actionCol,moduleCol,descCol,timeCol;
    @FXML public void initialize(){
        moduleFilter.setItems(FXCollections.observableArrayList("All","Authentication","KYC Validation","User Management","Validation History","Settings"));moduleFilter.setValue("All");
        actionFilter.setItems(FXCollections.observableArrayList("All","LOGIN_SUCCESS","LOGIN_FAILURE","LOGOUT","PAN_VALIDATION","PAN_VALIDATION_FAILURE","AADHAAR_VALIDATION","AADHAAR_VALIDATION_FAILURE","USER_CREATE","USER_UPDATE","USER_DELETE","CLEAR_HISTORY","CLEAR_LOGS","CSV_EXPORT","RECORD_DELETION"));actionFilter.setValue("All");
        userCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getUsername()));
        actionCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getAction()));
        moduleCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getModule()));
        descCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getDescription()));
        timeCol.setCellValueFactory(c->new SimpleStringProperty(DateUtil.formatDateTime(c.getValue().getCreatedAt())));
        loadData();
    }
    private void loadData(){String s=searchField!=null?searchField.getText():"";String m=moduleFilter!=null?moduleFilter.getValue():"All";String a=actionFilter!=null?actionFilter.getValue():"All";logsTable.setItems(FXCollections.observableArrayList(AuditService.getLogsByFilters(s,m,a)));}
    @FXML public void handleSearch(){loadData();}
    @FXML public void handleClearSearch(){searchField.clear();moduleFilter.setValue("All");actionFilter.setValue("All");loadData();}
}
