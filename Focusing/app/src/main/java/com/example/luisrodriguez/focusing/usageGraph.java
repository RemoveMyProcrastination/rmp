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


public class usageGraph extends AppCompatActivity {

    BarChart barChart;

    String[] values = new String[20];
    Button newButt;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_weekly_graph);
        addListenerOnButton();

        barChart = (BarChart) findViewById(R.id.testGraph);

        ArrayList<BarEntry> barEntries = new ArrayList<>();


        ArrayList<entry> dailyData = new ArrayList<>();
        entry n1 = new entry("M", 175);
        dailyData.add(n1);
        entry e1 = new entry("T", 90);
        dailyData.add(e1);
        entry e2 = new entry("W", 100);
        dailyData.add(e2);
        entry e3 = new entry("Th", 120);
        dailyData.add(e3);
        entry e4 = new entry("F", 125);
        dailyData.add(e4);
        entry e5 = new entry("S", 110);
        dailyData.add(e5);
        entry e6 = new entry("Su", 200);


        for (int i = 0; i < dailyData.size(); i++) {
            Float value = dailyData.get(i).getValue();
            String appName = dailyData.get(i).getAppName();
            values[i] = appName;


            barEntries.add(new BarEntry(i,value));
        }


        XAxis xAxis = barChart.getXAxis();
        xAxis.setGranularity(.5f);
        xAxis.setValueFormatter(new MyAxisValueFormatter(values));
        YAxis yAxis = barChart.getAxisLeft();

        LimitLine limitLine = new LimitLine(120,"Procrastination Limit");
        limitLine.setLineColor(Color.RED);
        limitLine.setLineWidth(2f);
        limitLine.setTextSize(4f);
        yAxis.addLimitLine(limitLine);





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
        barChart.setNoDataText("");


        // barChart.invalidate(); // refresh
    }

    protected void addListenerOnButton(){
        final Context context = this;
        newButt = (Button) findViewById(R.id.button3);

        newButt.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                Intent intent = new Intent(context, dailyGraph.class);
                startActivity(intent);
            }
        });

    }
}
