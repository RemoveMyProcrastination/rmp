package com.example.syukrina.focus;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.Button;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;

/**
 * Created by SYUKRINA on 12/5/2016.
 */



public class usageGraph extends AppCompatActivity {

    BarChart barChart;
    BarChart horChart;
    String[] values = new String[20];
    Button button;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_usage_graph);

        barChart = (BarChart) findViewById(R.id.testGraph);
        horChart = (BarChart) findViewById(R.id.weekGraph);
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


        XAxis xAxis = horChart.getXAxis();
        xAxis.setGranularity(1f);
        xAxis.setValueFormatter(new MyAxisValueFormatter(values));




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
        horChart.setData(data);
        horChart.setDrawGridBackground(true);
        horChart.setFitBars(true);
        horChart.invalidate();

        // barChart.invalidate(); // refresh
    }
}



