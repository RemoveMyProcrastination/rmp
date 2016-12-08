package com.example.josephjennings.applicationinfo;


import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;


import java.io.FileNotFoundException;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void ApplicationInfo(View view){
        PackageManager pm = getPackageManager();
        List<PackageInfo> list = pm.getInstalledPackages(0);

        for(PackageInfo pi : list) {
            try {
                ApplicationInfo ai = pm.getApplicationInfo(pi.packageName, 0);

                System.out.println(">>>>>>packages is<<<<<<<<" + ai.flags);

                if ((ai.flags & ApplicationInfo.FLAG_SYSTEM) != 0) {
                    System.out.println(">>>>>>packages is system package" + pi.packageName);
                }
            }
            catch (PackageManager.NameNotFoundException ex){
                System.out.println("App not found");
            }
        }
    }
}
