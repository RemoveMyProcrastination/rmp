package com.example.syukrina.focus;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

public class HomeActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_page);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
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
            Intent intent = new Intent(HomeActivity.this, HomePage.class);
            startActivity(intent);
            // Handle the camera action
        } else if (id == R.id.nav_faces) {
            Intent intent = new Intent(HomeActivity.this, FacesActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_person) {
            Intent intent = new Intent(HomeActivity.this, AboutActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_home) {
            Intent intent = new Intent(HomeActivity.this, HomePage.class);
            startActivity(intent);

        } else if (id == R.id.nav_manage) {
            Intent intent = new Intent(HomeActivity.this, SettingActivity.class);
            startActivity(intent);

        } else if (id == R.id.nav_help) {
            Intent intent = new Intent(HomeActivity.this, HelpActivity.class);
            startActivity(intent);

        }

        return true;
    }
}
