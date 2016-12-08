package com.example.syukrina.focus;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.Button;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.LimitLine;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.utils.ColorTemplate;

import org.json.JSONException;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;

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
 * Created by SYUKRINA on 12/5/2016.
 */



public class usageGraph extends AppCompatActivity {

    BarChart barChart;

    String[] values = new String[20];
    Button button;
    LimitLine limitLine;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.content_home_page);

        barChart = (BarChart) findViewById(R.id.testGraph);
        //ArrayList<entry>dailyData = weeklyData();


        ArrayList<BarEntry> barEntries = new ArrayList<>();


        ArrayList<entry> dailyData = new ArrayList<>();
        entry n1 = new entry("Netflix", 20);
        dailyData.add(n1);
        entry e1 = new entry("YouTube", 30);
        dailyData.add(e1);
        entry e2 = new entry("Facebook", 40);
        dailyData.add(e2);


        for (int i = 0; i < dailyData.size(); i++) {
            Float value = dailyData.get(i).getValue();
            String appName = dailyData.get(i).getAppName();
            values[i] = appName;


            barEntries.add(new BarEntry(i,value));
        }


        XAxis xAxis = barChart.getXAxis();
        xAxis.setGranularity(1f);
        xAxis.setValueFormatter(new MyAxisValueFormatter(values));
        YAxis yaxis = barChart.getAxisLeft();

        LimitLine limitline = new LimitLine(20f, "Daily Goal");
        limitline.setLineColor(Color.RED);
        limitline.setTextSize(12f);
        limitline.setLineWidth(4f);

        yaxis.addLimitLine(limitline);




        BarDataSet set = new BarDataSet(barEntries, "WeeklyUsage");


        set.setColors(ColorTemplate.VORDIPLOM_COLORS);

        BarData data = new BarData(set);

        data.setBarWidth(0.5f); // set custom bar width
           /* barChart.setData(data);
            barChart.setDrawGridBackground(true);
            barChart.setFitBars(true);
            barChart.notifyDataSetChanged();
            barChart.invalidate();
            */
        barChart.setData(data);
        barChart.setDrawGridBackground(true);
        barChart.setFitBars(true);
        barChart.invalidate();

        // barChart.invalidate(); // refresh
    }




}



