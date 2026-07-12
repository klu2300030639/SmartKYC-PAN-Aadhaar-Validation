package com.smartkyc.utils;
import java.sql.Timestamp;
import java.time.format.DateTimeFormatter;
public class DateUtil {
    private static final DateTimeFormatter FMT=DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    public static String formatDateTime(Timestamp ts){ return ts==null?"N/A":ts.toLocalDateTime().format(FMT); }
}
