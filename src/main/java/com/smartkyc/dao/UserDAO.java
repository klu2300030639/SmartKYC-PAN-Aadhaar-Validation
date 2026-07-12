package com.smartkyc.dao;
import com.smartkyc.model.User;
import java.util.List;
public interface UserDAO {
    User findById(int userId); User findByUsername(String username); User findByEmail(String email);
    List<User> findAll(); List<User> searchUsers(String query);
    boolean insert(User user); boolean update(User user); boolean delete(int userId);
    boolean updateStatus(int userId,String status); boolean resetPassword(int userId,String hash);
    int getTotalUsersCount();
}
