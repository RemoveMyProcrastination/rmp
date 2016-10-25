package com.rmp.demogetopenapp;

import android.app.IntentService;
import android.content.Intent;


/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p>
 * TODO: Actually log the open app.
 */
public class LogOpenApp extends IntentService {

    public LogOpenApp() {
        super("LogOpenApp");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            System.out.println("hello world!");
        }
    }

}
