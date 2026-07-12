package com.smartkyc.controller;
import com.smartkyc.dao.UserDAO;
import com.smartkyc.dao.UserDAOImpl;
import com.smartkyc.model.LoginRecord;
import com.smartkyc.model.ValidationRecord;
import com.smartkyc.service.AuthenticationService;
import com.smartkyc.service.HistoryService;
import com.smartkyc.utils.DateUtil;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import java.util.List;
public class DashboardController {
    @FXML private Label totalValidationsLabel,todayValidationsLabel,totalUsersLabel,aadhaarStatsLabel;
    @FXML private Label panValidLabel,panInvalidLabel,aadhaarValidLabel,aadhaarInvalidLabel;
    @FXML private PieChart validationPieChart;
    @FXML private BarChart<String,Number> validationBarChart;
    @FXML private TableView<ValidationRecord> recentValidationsTable;
    @FXML private TableColumn<ValidationRecord,String> valDocTypeCol,valDocNumCol,valStatusCol,valTimeCol;
    @FXML private TableView<LoginRecord> recentLoginsTable;
    @FXML private TableColumn<LoginRecord,String> loginUserCol,loginStatusCol,loginIpCol,loginTimeCol;
    private final UserDAO userDAO=new UserDAOImpl();
    @FXML public void initialize(){loadKPIs();loadCharts();loadTables();}
    private void loadKPIs(){
        int pv=HistoryService.getCount("PAN","Valid"),pi=HistoryService.getCount("PAN","Invalid");
        int av=HistoryService.getCount("Aadhaar","Valid"),ai=HistoryService.getCount("Aadhaar","Invalid");
        totalValidationsLabel.setText(String.valueOf(HistoryService.getTotalCount()));
        todayValidationsLabel.setText(String.valueOf(HistoryService.getTodayCount()));
        totalUsersLabel.setText(String.valueOf(userDAO.getTotalUsersCount()));
        aadhaarStatsLabel.setText(av+" / "+ai);
        panValidLabel.setText("Valid: "+pv);panInvalidLabel.setText("Invalid: "+pi);
        aadhaarValidLabel.setText("Valid: "+av);aadhaarInvalidLabel.setText("Invalid: "+ai);
    }
    private void loadCharts(){
        int tp=HistoryService.getCount("PAN","Valid")+HistoryService.getCount("PAN","Invalid");
        int ta=HistoryService.getCount("Aadhaar","Valid")+HistoryService.getCount("Aadhaar","Invalid");
        var pie=FXCollections.<PieChart.Data>observableArrayList();
        if(tp>0)pie.add(new PieChart.Data("PAN ("+tp+")",tp));
        if(ta>0)pie.add(new PieChart.Data("Aadhaar ("+ta+")",ta));
        if(pie.isEmpty())pie.add(new PieChart.Data("No Data",1));
        validationPieChart.setData(pie);
        XYChart.Series<String,Number> s=new XYChart.Series<>();
        s.getData().add(new XYChart.Data<>("Valid",HistoryService.getCount("PAN","Valid")+HistoryService.getCount("Aadhaar","Valid")));
        s.getData().add(new XYChart.Data<>("Invalid",HistoryService.getCount("PAN","Invalid")+HistoryService.getCount("Aadhaar","Invalid")));
        validationBarChart.getData().clear();validationBarChart.getData().add(s);
    }
    private void loadTables(){
        List<ValidationRecord> vals=HistoryService.getRecentValidations(5);
        recentValidationsTable.setItems(FXCollections.observableArrayList(vals));
        valDocTypeCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getDocumentType()));
        valDocNumCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getDocumentNumber()));
        valStatusCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getStatus()));
        valTimeCol.setCellValueFactory(c->new SimpleStringProperty(DateUtil.formatDateTime(c.getValue().getValidatedAt())));
        List<LoginRecord> logins=AuthenticationService.getRecentLoginAttempts(5);
        recentLoginsTable.setItems(FXCollections.observableArrayList(logins));
        loginUserCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getUsername()));
        loginStatusCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getLoginStatus()));
        loginIpCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getIpAddress()));
        loginTimeCol.setCellValueFactory(c->new SimpleStringProperty(DateUtil.formatDateTime(c.getValue().getLoginTime())));
    }
}
