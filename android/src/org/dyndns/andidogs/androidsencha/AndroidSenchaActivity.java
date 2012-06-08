package org.dyndns.andidogs.androidsencha;

import org.apache.cordova.DroidGap;

import android.os.Bundle;

public class AndroidSenchaActivity extends DroidGap {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setIntegerProperty("loadUrlTimeoutValue", 60000);
        super.loadUrl("file:///android_asset/www/index.html");
    }
}
