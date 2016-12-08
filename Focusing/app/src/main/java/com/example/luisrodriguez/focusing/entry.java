package com.example.luisrodriguez.focusing;

/**
 * Created by adam on 12/8/2016.
 */

public class entry {
    private String appName;
    private float value;


    public entry(String appName, float value) {
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

