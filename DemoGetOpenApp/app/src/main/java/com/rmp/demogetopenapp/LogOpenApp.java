package com.rmp.demogetopenapp;

import android.app.IntentService;
import android.app.usage.UsageStats;
import android.app.usage.UsageStatsManager;
import android.content.Context;
import android.content.Intent;
import android.provider.Settings;

import java.util.Calendar;
import java.util.List;





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
            long check = 0;
            UsageStatsManager usm = getUsageStatsManager(this);
            Calendar calendar = Calendar.getInstance();
            long endTime = calendar.getTimeInMillis();
            //calendar.add(Calendar.DAY_OF_MONTH, -3);
            long startTime = calendar.getTimeInMillis() - 60000;
            //TODO Create a time counter for each day. Poll usage stats for every hour, subtract previous results.
            
            List<UsageStats> usageStatsList = usm.queryUsageStats(UsageStatsManager.INTERVAL_BEST,startTime,endTime);


            for (UsageStats u : usageStatsList){
                if(u.getTotalTimeInForeground() != check) {
                    System.out.println(u.getPackageName() + "\t" + "ForegroundTime: "
                            + u.getTotalTimeInForeground()/6000);
                }
            }



        }
    }

    private static UsageStatsManager getUsageStatsManager(Context context){
        UsageStatsManager usm = (UsageStatsManager) context.getSystemService("usagestats");
        return usm;
    }
}
