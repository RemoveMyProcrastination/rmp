package com.rmp.demogetopenapp;

import android.app.IntentService;
import android.app.usage.UsageStats;
import android.app.usage.UsageStatsManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;


import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Calendar;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.TimeUnit;




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

            // Initialize usage stats
            UsageStatsManager usm = getUsageStatsManager(this);
            //Initialize package manager
            PackageManager pm = getPackageManager();


            // Set start and stop time for usage stats
            Calendar calendar = Calendar.getInstance();
            long endTime = calendar.getTimeInMillis();
            calendar.set(Calendar.HOUR_OF_DAY, 0);
            calendar.set(Calendar.MINUTE,0);
            calendar.set(Calendar.SECOND,0);
            calendar.set(Calendar.MILLISECOND,0);
            long startTime = calendar.getTimeInMillis();


            //List of Apps used in time interval
            List<UsageStats> usageStatsList = usm.queryUsageStats(UsageStatsManager.INTERVAL_BEST,startTime,endTime);


            for (UsageStats u : usageStatsList){
                //If app was used
                if(u.getTotalTimeInForeground() != 0) {
                    String tst = u.getPackageName();

                    // Convert time from millisec to hours, min, sec
                    long millis = u.getTotalTimeInForeground();
                    long hour = TimeUnit.MILLISECONDS.toHours(millis);
                    millis -= TimeUnit.HOURS.toMillis(hour);
                    long min = TimeUnit.MILLISECONDS.toMinutes(millis);
                    millis -= TimeUnit.MINUTES.toMillis(min);
                    long sec = TimeUnit.MILLISECONDS.toSeconds(millis);

                    try {
                        //Check if system app
                        ApplicationInfo ai = pm.getApplicationInfo(u.getPackageName(), 0);
                        if ((ai.flags & ApplicationInfo.FLAG_SYSTEM) == 0) {
                            try{
                                String appname = pm.getApplicationLabel(ai).toString();
                                //Format into JSON
                                JSONObject application = new JSONObject();
                                JSONArray time = new JSONArray();
                                //time.put(hour);
                                time.put(min);
                                //time.put(sec);
                                application.put(appname, time);
                                String newapp = application.toString();
                                newapp = newapp.replace("[","");
                                newapp = newapp.replace("]","");
                                sendData(newapp);
                                System.out.println(newapp);
                            } catch(JSONException e){
                                e.printStackTrace();
                            }

                        }
                    }
                    catch (PackageManager.NameNotFoundException ex){
                        System.out.println("App not found");
                    }
                }
            }



        }
        getData();
    }


    protected void sendData(String application){
        try {
            //Connect to the URL
            HttpURLConnection urlConnection;
            String serverAddr = "http://ec2-35-160-174-113.us-west-2.compute.amazonaws.com:5000/usage/Joby/";
            URL url = new URL(serverAddr);
            urlConnection = (HttpURLConnection) url.openConnection();

            //Format for JSON and set method to Put
            urlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            urlConnection.setRequestMethod("PUT");

            //Write to buffer and send
            OutputStreamWriter out = new OutputStreamWriter(urlConnection.getOutputStream());
            out.write(application);
            out.close();

            //Response code
            int responseCode = urlConnection.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode + " | " + urlConnection.getResponseMessage());

            //close connection
            urlConnection.disconnect();

        } catch (MalformedURLException badurl) {
            System.out.println("Bad URL");
        } catch (IOException io) {
            System.out.println("Not sending");

        }
    }

    public void getData() {
        try {

            //Connect to URL
            HttpURLConnection urlConnection;
            String serverAddr = "http://ec2-35-160-174-113.us-west-2.compute.amazonaws.com:5000/wgraph/Joby/";
            URL url = new URL(serverAddr);
            urlConnection = (HttpURLConnection) url.openConnection();

            //Format for json and set method to GET
            urlConnection.setRequestMethod("GET");
            //urlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8\"");

            BufferedReader rd;
            StringBuilder sb;
            String line;

            //Read buffer from server and oyt into string
            rd  = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            sb = new StringBuilder();
            while ((line = rd.readLine()) != null)
            {
                sb.append(line + '\n');
            }

            String apps = sb.toString();
            JSONObject jsonObject;
            JSONObject jsonObject1;
            JSONArray jsonArray;

            int i = 0;

            //Put into JSON format
            try {

                //Get Appdate from entire object
                jsonObject = new JSONObject(apps);
                jsonArray = jsonObject.getJSONArray("days");

                //Array of applications
                String[] applications = new String[jsonArray.length()];

                //Array of minutes
                float[] minutes = new float[jsonArray.length()];
                System.out.println(jsonObject);


                System.out.println(jsonArray);

                //iterate though Appdata keys, getting total
                for(int count = 0; count < jsonArray.length(); count++) {

                    jsonObject1 = jsonArray.getJSONObject(count);
                    for(Iterator<String> iter = jsonObject1.keys();iter.hasNext();) {
                        String key = iter.next();
                        float min = jsonObject1.getInt(key);
                        applications[i]= key;
                        minutes[i] = min;
                        i++;

                    }



                }


                for(int j = 0; j < i; j++) {
                    System.out.println(applications[j]);
                    System.out.println(minutes[j]);
                }



            }
            catch (JSONException js){
                System.out.println("Fuck");
            }

            //Response code
            int responseCode = urlConnection.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode + " | " + urlConnection.getResponseMessage());

            urlConnection.disconnect();

        } catch (MalformedURLException badurl) {
            System.out.println("Bad URL");
        } catch (IOException io) {
            System.out.println("Not Receiving");

        }
    }

    private static UsageStatsManager getUsageStatsManager(Context context){
        UsageStatsManager usm = (UsageStatsManager) context.getSystemService("usagestats");
        return usm;
    }
}
