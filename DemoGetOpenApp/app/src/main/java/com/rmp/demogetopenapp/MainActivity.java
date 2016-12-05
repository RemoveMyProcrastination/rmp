package com.rmp.demogetopenapp;

import android.app.AlarmManager;
import android.app.AppOpsManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.Switch;

import static android.provider.Settings.ACTION_USAGE_ACCESS_SETTINGS;

public class MainActivity extends AppCompatActivity {

    public static long LOOP_WAIT_MILLIS = 1000 * 600;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Check if permission is already set. If not take user to settings
        AppOpsManager appOps = (AppOpsManager) this.getSystemService(Context.APP_OPS_SERVICE);
        int mode = appOps.checkOpNoThrow("android:get_usage_stats", android.os.Process.myUid(), this.getPackageName());
        boolean granted = mode == AppOpsManager.MODE_ALLOWED;
        if( granted == false) {
            Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
            startActivity(intent);
        }




        Switch looper = (Switch) findViewById(R.id.loopLogButton);
        looper.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                toggleLoopLogging(buttonView, isChecked);
            }
        });
    }

    protected void planToLogOpenApp(View v) {
        System.out.println("Planning to say hello.");

        Intent i = new Intent(this, LogOpenApp.class);
        startService(i);
    }


    protected void toggleLoopLogging(View v, boolean loop) {

        Context ctx = this.getApplicationContext();
        AlarmManager amgr = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);

        if (amgr == null) {
            System.out.println("Error: could not load alarm manager.");
            return;
        }

        Intent intent = new Intent(this, LogOpenApp.class);
        PendingIntent pi = PendingIntent.getService(ctx, 0, intent, 0);


        if (loop) {
            // start looping

            amgr.setInexactRepeating(AlarmManager.ELAPSED_REALTIME, LOOP_WAIT_MILLIS, LOOP_WAIT_MILLIS, pi);
            System.out.println("Started looping.");

        } else {
            // stop looping

            amgr.cancel(pi);
            System.out.println("Stopped looping.");
        }

    }

}
