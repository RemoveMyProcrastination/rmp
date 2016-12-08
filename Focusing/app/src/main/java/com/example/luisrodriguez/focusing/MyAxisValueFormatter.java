package com.example.luisrodriguez.focusing;

import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;

/**
 * Created by adam on 12/8/2016.
 */

public class MyAxisValueFormatter implements IAxisValueFormatter {
    private String[] mValues;

    public MyAxisValueFormatter(String[] values) {
        this.mValues = values;
    }

    @Override
    public String getFormattedValue(float value, AxisBase axis) {
        // "value" represents the position of the label on the axis (x or y)
        return mValues[(int) value];
    }

    /** this is only needed if numbers are returned, else return 0 */
    @Override
    public int getDecimalDigits() { return 0; }
}
