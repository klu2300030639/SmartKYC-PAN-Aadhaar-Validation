package com.smartkyc.validator;
public class InputNormalizer {
    public static String normalize(String input){ return input==null?"":input.trim().toUpperCase(); }
}
