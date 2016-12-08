package com.example.adamt.bargrahp;

/**
 * Created by adam on 12/4/2016.
 */
public class Entry {
    private String appName;
    private float value;


    public Entry(String appName, float value) {
        this.appName = appName;
        this.value = value;
    }

    String getAppName() {
        return appName;
    }

    float getValue() {
        return value;
    }

}
