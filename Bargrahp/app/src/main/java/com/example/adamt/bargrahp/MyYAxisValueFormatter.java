package com.example.adamt.bargrahp;

import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;

import java.text.DecimalFormat;

/**
 * Created by adam on 12/4/2016.
 */

public class MyYAxisValueFormatter implements IAxisValueFormatter {

    private DecimalFormat mFormat;

    public MyYAxisValueFormatter() {

        // format values to 1 decimal digit
        mFormat = new DecimalFormat("###,###,##0.0");
    }

    @Override
    public String getFormattedValue(float value, AxisBase axis) {
        // "value" represents the position of the label on the axis (x or y)
        return mFormat.format(value) + " $";
    }

    /** this is only needed if numbers are returned, else return 0 */
    @Override
    public int getDecimalDigits() { return 1; }
}
