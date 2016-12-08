package com.example.luisrodriguez.focusing;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.LimitLine;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;

/**
 * Created by adam on 12/8/2016.
 */

public class dailyGraph extends AppCompatActivity {

    BarChart newChart;

    String[] values = new String[20];
    Button butt6;
    LimitLine limitLine;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_daily_graph);
        addListenerOnButton();
        newChart = (BarChart) findViewById(R.id.newGraph);

        ArrayList<BarEntry> barEntries = new ArrayList<>();


        ArrayList<entry> dailyData = new ArrayList<>();
        entry n1 = new entry("Netflix", 20);
        dailyData.add(n1);
        entry e1 = new entry("YouTube", 50);
        dailyData.add(e1);
        entry e2 = new entry("Facebook", 40);
        dailyData.add(e2);
        entry e3 = new entry("Snapchat", 25);
        dailyData.add(e3);
        entry e4 = new entry("Instagram", 40);


        for (int i = 0; i < dailyData.size(); i++) {
            Float value = dailyData.get(i).getValue();
            String appName = dailyData.get(i).getAppName();
            values[i] = appName;


            barEntries.add(new BarEntry(i, value));
        }


        XAxis xAxis = newChart.getXAxis();
        xAxis.setGranularity(1f);
        xAxis.setValueFormatter(new MyAxisValueFormatter(values));

        YAxis yAxis = newChart.getAxisLeft();

        LimitLine limitLine = new LimitLine(30, "Procrastination Limit");
        limitLine.setLineColor(Color.RED);
        limitLine.setLineWidth(2f);
        limitLine.setTextSize(4f);
        yAxis.addLimitLine(limitLine);


        BarDataSet set = new BarDataSet(barEntries, "Daily Usage(minutes)");


        set.setColors(ColorTemplate.VORDIPLOM_COLORS);

        BarData data = new BarData(set);

        data.setBarWidth(0.5f); // set custom bar width
           /* barChart.setData(data);
            barChart.setDrawGridBackground(true);
            barChart.setFitBars(true);
            barChart.notifyDataSetChanged();
            barChart.invalidate();
            */
        newChart.setData(data);
        newChart.setDrawGridBackground(true);
        newChart.setFitBars(true);
        newChart.invalidate();
        newChart.setNoDataText("");


        // barChart.invalidate(); // refresh
    }

    protected void addListenerOnButton() {
        final Context context = this;
        butt6 = (Button) findViewById(R.id.button4);

        butt6.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(context, usageGraph.class);
                startActivity(intent);
            }
        });
    }
}
