package com.estimote.proximitycontent;

import android.app.Application;

import com.estimote.proximitycontent.estimote.BeaconID;
import com.estimote.sdk.EstimoteSDK;
import com.estimote.proximitycontent.estimote.BeaconNotificationsManager;

//
// Running into any issues? Drop us an email to: contact@estimote.com
//

public class MyApplication extends Application {


    @Override
    public void onCreate() {
        super.onCreate();

        // TODO: put your App ID and App Token here
        // You can get them by adding your app on https://cloud.estimote.com/#/apps
        EstimoteSDK.initialize(getApplicationContext(), "team-13-ekq", "7e48b8789c72c234a6615883ac783146");

        // uncomment to enable debug-level logging
        // it's usually only a good idea when troubleshooting issues with the Estimote SDK
//        EstimoteSDK.enableDebugLogging(true);
    }


}
