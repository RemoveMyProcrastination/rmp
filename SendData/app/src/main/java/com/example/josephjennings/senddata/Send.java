package com.example.josephjennings.senddata;

import android.app.IntentService;
import android.content.Intent;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by josephjennings on 11/23/16.
 */

public class Send extends IntentService {

    public Send() {
        super("Send");
    }


    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            System.out.println("Test");

            sendData();
            getData();



        }
    }

    public void sendData() {
        try {
            HttpURLConnection urlConnection;
            //OutputStream out;
            String serverAddr = "http://ec2-35-160-174-113.us-west-2.compute.amazonaws.com:5000/usage/Joby/";
            URL url = new URL(serverAddr);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            urlConnection.setRequestMethod("PUT");

            OutputStreamWriter out = new OutputStreamWriter(urlConnection.getOutputStream());
            out.write("{\"com.rmp.demogetopenapp\":[5]}");
            out.close();

            //out = new BufferedOutputStream(urlConnection.getOutputStream());
            //out.write(application.getBytes("UTF-8"));

            int responseCode = urlConnection.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode + " | " + urlConnection.getResponseMessage());

            urlConnection.disconnect();

        } catch (MalformedURLException badurl) {
            System.out.println("Bad URL");
        } catch (IOException io) {
            System.out.println("Not sending");

        }
    }

    public void getData() {
        try {
            HttpURLConnection urlConnection;
            BufferedReader rd  = null;
            StringBuilder sb = null;
            String line = null;

            String serverAddr = "http://ec2-35-160-174-113.us-west-2.compute.amazonaws.com:5000/get/Yogitha/";
            URL url = new URL(serverAddr);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod("GET");
            urlConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8\"");


            rd  = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            sb = new StringBuilder();

            while ((line = rd.readLine()) != null)
            {
                sb.append(line + '\n');
            }

            String apps = sb.toString();
            JSONObject jsonObject = null;
            try {
                jsonObject = new JSONObject(apps);
                System.out.println(jsonObject.getString("Appdata"));

            }
            catch (JSONException js){
                System.out.println("Fuck");
            }

            int responseCode = urlConnection.getResponseCode();
            System.out.println("HTTP Response Code: " + responseCode + " | " + urlConnection.getResponseMessage());

            urlConnection.disconnect();

        } catch (MalformedURLException badurl) {
            System.out.println("Bad URL");
        } catch (IOException io) {
            System.out.println("Not sending");

        }
    }
}

