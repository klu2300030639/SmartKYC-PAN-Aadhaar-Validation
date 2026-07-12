package com.smartkyc.dao;
import java.util.Map;
public interface SettingsDAO {
    String get(String key); boolean set(String key,String value); Map<String,String> getAll();
}
