package com.example.adamt.bargrahp;

import android.graphics.Color;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.components.LimitLine;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.DefaultAxisValueFormatter;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;


import static android.R.attr.data;
import static android.R.attr.description;
import static android.R.attr.entryValues;
import static android.R.attr.value;

public class MainActivity extends AppCompatActivity {

    BarChart barChart;
    BarChart horChart;
    String[] values = new String[20];
    LimitLine limitLine;





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        barChart = (BarChart) findViewById(R.id.testGraph);
        horChart = (BarChart) findViewById(R.id.weekGraph);
        ArrayList<BarEntry> barEntries = new ArrayList<>();


        ArrayList<Entry> dailyData = new ArrayList<>();
        Entry n1 = new Entry("Netflix", 20);
        dailyData.add(n1);
        Entry e1 = new Entry("YouTube", 30);
        dailyData.add(e1);
        Entry e2 = new Entry("Facebook", 40);
        dailyData.add(e2);
        Entry e3 = new Entry("Snapchat", 50);
        dailyData.add(e3);
        Entry e4 = new Entry("Instagram", 60);
        dailyData.add(e4);


        for (int i = 0; i < dailyData.size(); i++) {
            Float value = dailyData.get(i).getValue();
            String appName = dailyData.get(i).getAppName();
            values[i] = appName;


            barEntries.add(new BarEntry(i,value));
        }


            XAxis xAxis = horChart.getXAxis();
            xAxis.setGranularity(1f);
            xAxis.setValueFormatter(new MyAxisValueFormatter(values));
            YAxis yAxis = horChart.getAxisLeft();

            LimitLine limitLine = new LimitLine(20f, "Procrastination Goal");
            limitLine.setLineColor(Color.RED);
            limitLine.setLineWidth(4f);
            limitLine.setTextColor(Color.BLACK);
            limitLine.setTextSize(12f);
            yAxis.addLimitLine(limitLine);






            BarDataSet set = new BarDataSet(barEntries, "WeeklyUsage");
            String desc = "usage";

            set.setColors(ColorTemplate.VORDIPLOM_COLORS);

            BarData data = new BarData(set);

            data.setBarWidth(.5f); // set custom bar width
           /* barChart.setData(data);
            barChart.setDrawGridBackground(true);
            barChart.setFitBars(true);
            barChart.notifyDataSetChanged();
            barChart.invalidate();
            */
            horChart.setData(data);
            horChart.setDrawGridBackground(true);
            horChart.setFitBars(true);
            horChart.invalidate();
            horChart.setVisibleXRangeMaximum(20); // allow 20 values to be displayed at once on the x-axis, not more
            horChart.setDragEnabled(true);
            horChart.setTouchEnabled(true);
            horChart.setDescription(");


        // barChart.invalidate(); // refresh


        }


    }

