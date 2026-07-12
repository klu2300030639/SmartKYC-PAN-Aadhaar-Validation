package com.smartkyc.controller;
import com.smartkyc.model.ValidationRecord;
import com.smartkyc.service.*;
import com.smartkyc.utils.DateUtil;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.stage.FileChooser;
import java.io.File;
import java.util.List;
public class ValidationHistoryController {
    @FXML private TextField searchField;
    @FXML private ComboBox<String> docTypeFilter,statusFilter;
    @FXML private TableView<ValidationRecord> historyTable;
    @FXML private TableColumn<ValidationRecord,String> docTypeCol,docNumCol,statusCol,reasonCol,timeCol;
    @FXML public void initialize(){
        docTypeFilter.setItems(FXCollections.observableArrayList("All","PAN","Aadhaar"));docTypeFilter.setValue("All");
        statusFilter.setItems(FXCollections.observableArrayList("All","Valid","Invalid"));statusFilter.setValue("All");
        docTypeCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getDocumentType()));
        docNumCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getDocumentNumber()));
        statusCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getStatus()));
        reasonCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getReason()));
        timeCol.setCellValueFactory(c->new SimpleStringProperty(DateUtil.formatDateTime(c.getValue().getValidatedAt())));
        loadData();
    }
    private void loadData(){String s=searchField!=null?searchField.getText():"";String dt=docTypeFilter!=null?docTypeFilter.getValue():"All";String st=statusFilter!=null?statusFilter.getValue():"All";historyTable.setItems(FXCollections.observableArrayList(HistoryService.getHistoryByFilters(s,dt,st)));}
    @FXML public void handleSearch(){loadData();}
    @FXML public void handleClearSearch(){searchField.clear();docTypeFilter.setValue("All");statusFilter.setValue("All");loadData();}
    @FXML public void handleDelete(){
        ValidationRecord sel=historyTable.getSelectionModel().getSelectedItem();
        if(sel==null){AlertService.showWarning("No Selection","Select Record","Please select a record to delete.");return;}
        if(AlertService.showConfirmation("Delete","Confirm","Delete record for "+sel.getDocumentNumber()+"?")){if(HistoryService.deleteRecord(sel.getValidationId()))loadData();else AlertService.showError("Error","Failed","Could not delete record.");}
    }
    @FXML public void handleExportCSV(){
        FileChooser fc=new FileChooser();fc.setTitle("Save CSV");fc.setInitialFileName("kyc_history.csv");fc.getExtensionFilters().add(new FileChooser.ExtensionFilter("CSV","*.csv"));
        File f=fc.showSaveDialog(historyTable.getScene().getWindow());
        if(f!=null){if(CSVExportService.exportValidationHistory(HistoryService.getHistory(),f.getAbsolutePath()))AlertService.showInfo("Exported","Success","Exported to: "+f.getAbsolutePath());else AlertService.showError("Error","Failed","Could not export CSV.");}
    }
}
