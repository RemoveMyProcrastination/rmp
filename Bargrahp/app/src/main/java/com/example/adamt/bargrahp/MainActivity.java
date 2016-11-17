package com.example.adamt.bargrahp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    BarChart barChart;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        barChart = (BarChart) findViewById(R.id.testGraph);
        ArrayList<BarEntry> barEntries = new ArrayList<>();
        barEntries.add(new BarEntry(44f, 0));
        barEntries.add(new BarEntry(23f, 1));
        barEntries.add(new BarEntry(10f, 2));
        barEntries.add(new BarEntry(22f, 3));
        barEntries.add(new BarEntry(50f, 4));
        barEntries.add(new BarEntry(30f, 5));
        barEntries.add(new BarEntry(11f, 6));

        BarDataSet set = new BarDataSet(barEntries,"WeeklyUsage");

        ArrayList<String> weekDays = new ArrayList<>();
        weekDays.add("Sunday");
        weekDays.add("Monnday");
        weekDays.add("Tuesday");
        weekDays.add("Wednesday");
        weekDays.add("Thursday");
        weekDays.add("Friday");
        weekDays.add("Saturday");

        BarData data = new BarData(set);
        data.setBarWidth(0.9f); // set custom bar width
        barChart.setData(data);
        barChart.setFitBars(true); // make the x-axis fit exactly all bars
        barChart.invalidate(); // refresh

    }


}
