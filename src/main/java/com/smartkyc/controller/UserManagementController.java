package com.smartkyc.controller;
import com.smartkyc.dao.UserDAO;
import com.smartkyc.dao.UserDAOImpl;
import com.smartkyc.model.User;
import com.smartkyc.security.PasswordHasher;
import com.smartkyc.service.*;
import com.smartkyc.utils.DateUtil;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import java.util.List;
public class UserManagementController {
    @FXML private TextField searchField,fullNameField,usernameField,emailField,phoneField,passwordField;
    @FXML private ComboBox<String> roleCombo,statusCombo;
    @FXML private TableView<User> usersTable;
    @FXML private TableColumn<User,String> idCol,nameCol,usernameCol,emailCol,roleCol,statusCol,createdCol;
    @FXML private Label formTitleLabel;
    private final UserDAO userDAO=new UserDAOImpl();
    private User selectedUser;
    @FXML public void initialize(){
        roleCombo.setItems(FXCollections.observableArrayList("Admin","User"));roleCombo.setValue("User");
        statusCombo.setItems(FXCollections.observableArrayList("Active","Inactive"));statusCombo.setValue("Active");
        idCol.setCellValueFactory(c->new SimpleStringProperty(String.valueOf(c.getValue().getUserId())));
        nameCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getFullName()));
        usernameCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getUsername()));
        emailCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getEmail()));
        roleCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getRole()));
        statusCol.setCellValueFactory(c->new SimpleStringProperty(c.getValue().getStatus()));
        createdCol.setCellValueFactory(c->new SimpleStringProperty(DateUtil.formatDateTime(c.getValue().getCreatedAt())));
        usersTable.getSelectionModel().selectedItemProperty().addListener((obs,old,nv)->{if(nv!=null)populateForm(nv);});
        loadUsers();
    }
    private void loadUsers(){String s=searchField!=null?searchField.getText().trim():"";usersTable.setItems(FXCollections.observableArrayList(s.isEmpty()?userDAO.findAll():userDAO.searchUsers(s)));}
    private void populateForm(User u){selectedUser=u;formTitleLabel.setText("Edit User");fullNameField.setText(u.getFullName());usernameField.setText(u.getUsername());emailField.setText(u.getEmail());phoneField.setText(u.getPhone()!=null?u.getPhone():"");roleCombo.setValue(u.getRole());statusCombo.setValue(u.getStatus());passwordField.clear();}
    @FXML public void handleSave(){
        String fn=fullNameField.getText().trim(),un=usernameField.getText().trim(),em=emailField.getText().trim(),ph=phoneField.getText().trim(),ro=roleCombo.getValue(),st=statusCombo.getValue(),pw=passwordField.getText();
        if(fn.isEmpty()||un.isEmpty()||em.isEmpty()){AlertService.showWarning("Validation","Required Fields","Full Name, Username and Email are required.");return;}
        if(selectedUser==null){
            if(pw.isEmpty()){AlertService.showWarning("Validation","Password Required","Password is required for new users.");return;}
            if(RegistrationService.register(fn,un,em,pw,ph,ro)){AlertService.showInfo("Success","User Created","User '"+un+"' created.");clearForm();loadUsers();}
            else AlertService.showError("Error","Failed","Username or email already exists.");
        }else{
            selectedUser.setFullName(fn);selectedUser.setEmail(em);selectedUser.setPhone(ph);selectedUser.setRole(ro);selectedUser.setStatus(st);
            if(userDAO.update(selectedUser)){if(!pw.isEmpty())userDAO.resetPassword(selectedUser.getUserId(),PasswordHasher.hash(pw));AuditService.log("USER_UPDATE","User Management","Updated user: "+un);AlertService.showInfo("Success","Updated","User '"+un+"' updated.");clearForm();loadUsers();}
            else AlertService.showError("Error","Failed","Could not update user.");
        }
    }
    @FXML public void handleDelete(){
        if(selectedUser==null){AlertService.showWarning("Select","No User","Please select a user to delete.");return;}
        if(AlertService.showConfirmation("Delete","Confirm","Delete user '"+selectedUser.getUsername()+"'?")){if(userDAO.delete(selectedUser.getUserId())){AuditService.log("USER_DELETE","User Management","Deleted user: "+selectedUser.getUsername());clearForm();loadUsers();}else AlertService.showError("Error","Failed","Could not delete user.");}
    }
    @FXML public void handleSearch(){loadUsers();}
    @FXML public void handleNewUser(){clearForm();formTitleLabel.setText("Add New User");}
    private void clearForm(){selectedUser=null;formTitleLabel.setText("User Details");fullNameField.clear();usernameField.clear();emailField.clear();phoneField.clear();passwordField.clear();roleCombo.setValue("User");statusCombo.setValue("Active");usersTable.getSelectionModel().clearSelection();}
}
