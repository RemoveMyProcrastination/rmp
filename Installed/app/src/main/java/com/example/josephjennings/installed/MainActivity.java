package com.example.josephjennings.installed;

import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.media.Image;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

import java.util.List;

import static com.example.josephjennings.installed.R.id.image;

public class MainActivity extends AppCompatActivity {

    ImageView image;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    protected void getApps(View view){
        PackageManager pm = getPackageManager();
        List<ApplicationInfo> packages = pm.getInstalledApplications(PackageManager.GET_META_DATA);

        for(ApplicationInfo packageinfo : packages) {
            if ((packageinfo.flags & ApplicationInfo.FLAG_SYSTEM) == 0) {
                System.out.println(pm.getApplicationLabel(packageinfo));
                image = (ImageView) findViewById(R.id.imageView);
                image.setImageDrawable(pm.getApplicationLogo(packageinfo));

            }
        }
    }
}
