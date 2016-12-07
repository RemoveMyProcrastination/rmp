package com.example.syukrina.focus;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.widget.TextView;

import com.github.mikephil.charting.charts.BarChart;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;

import java.util.ArrayList;

public class HomePage extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    BarChart barChart;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_page);

        setContentView(R.layout.activity_home_page);
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

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.home_page, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_timelapse) {
            Intent intent = new Intent(HomePage.this, HomePage.class);
            startActivity(intent);
            // Handle the camera action
        } else if (id == R.id.nav_faces) {
            Intent intent = new Intent(HomePage.this, FacesActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_person) {
            Intent intent = new Intent(HomePage.this, AboutActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_home) {
            Intent intent = new Intent(HomePage.this, HomePage.class);
            startActivity(intent);

        } else if (id == R.id.nav_manage) {
            Intent intent = new Intent(HomePage.this, SettingActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_help) {
            Intent intent = new Intent(HomePage.this, HelpActivity.class);
            startActivity(intent);

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }


    public class ScrollingActivity extends AppCompatActivity {

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.app_bar_home_page);
            Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
            setSupportActionBar(toolbar);
        }
    }
}