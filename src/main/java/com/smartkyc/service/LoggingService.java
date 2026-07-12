package com.smartkyc.service;
import com.smartkyc.config.ConfigurationManager;
import java.io.*;
import java.util.logging.*;
public class LoggingService {
    private static final Logger rootLogger=Logger.getLogger("");
    private static FileHandler fileHandler;
    public static void initialize(){
        try{
            String path=ConfigurationManager.getLogPath();
            File f=new File(path);if(f.getParentFile()!=null)f.getParentFile().mkdirs();
            for(Handler h:rootLogger.getHandlers())rootLogger.removeHandler(h);
            Formatter fmt=new SimpleFormatter(){
                private static final String FORMAT="[%1$tF %1$tT] [%2$-7s] %3$s %4$s%n";
                @Override public synchronized String format(LogRecord lr){String t="";if(lr.getThrown()!=null){StringWriter sw=new StringWriter();lr.getThrown().printStackTrace(new PrintWriter(sw));t=sw.toString();}return String.format(FORMAT,lr.getMillis(),lr.getLevel().getLocalizedName(),lr.getMessage(),t);}
            };
            fileHandler=new FileHandler(path,5000000,5,true);fileHandler.setFormatter(fmt);rootLogger.addHandler(fileHandler);
            ConsoleHandler ch=new ConsoleHandler();ch.setFormatter(fmt);rootLogger.addHandler(ch);
            rootLogger.setLevel(Level.INFO);
        }catch(IOException|SecurityException e){rootLogger.log(Level.SEVERE,"LoggingService init failed",e);}
    }
    public static void close(){if(fileHandler!=null)fileHandler.close();}
}
