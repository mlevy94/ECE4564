package com.estimote.proximitycontent;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.NumberPicker;

import com.estimote.proximitycontent.estimote.BeaconID;
import com.estimote.proximitycontent.estimote.BeaconNotificationsManager;
import com.estimote.proximitycontent.estimote.EstimoteCloudBeaconDetails;
import com.estimote.proximitycontent.estimote.EstimoteCloudBeaconDetailsFactory;
import com.estimote.proximitycontent.estimote.ProximityContentManager;
import com.estimote.sdk.SystemRequirementsChecker;
import com.estimote.sdk.cloud.model.Color;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

//
// Running into any issues? Drop us an email to: contact@estimote.com
//

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private boolean beaconNotificationsEnabled = false;
    private static final Map<Color, Integer> BACKGROUND_COLORS = new HashMap<>();

    static {
        BACKGROUND_COLORS.put(Color.MINT_COCKTAIL, android.graphics.Color.rgb(155, 186, 160));//Background of our mint green beacon
    }
    String usr2;//username for use in database
    int numb2;// number for use in database
    private static final int BACKGROUND_COLOR_NEUTRAL = android.graphics.Color.rgb(160, 169, 172);// base background

    private ProximityContentManager proximityContentManager;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);//creation of layout

        NumberPicker np = (NumberPicker)findViewById(R.id.np);//number picker for number and textview for displaying number
        final TextView tv = (TextView) findViewById(R.id.tv);

        np.setMinValue(0);
        np.setMaxValue(500);
        np.setWrapSelectorWheel(false);//min max and no wrapping

        final TextView tv2 = (TextView)findViewById(R.id.tv2);//proof of concept textview
        final EditText ed = (EditText)findViewById(R.id.username); //used for inputing username
        Button okbt = (Button)findViewById(R.id.okbt);//button creation

        okbt.setOnClickListener(new TextView.OnClickListener(){//on click button listener. saves username.

            public void onClick (View view){
                String usrnme = ed.getText().toString();
                tv2.setText(usrnme);
                usr2 = usrnme;


            }

        });
        np.setOnValueChangedListener(new NumberPicker.OnValueChangeListener() {
            @Override
            public void onValueChange (NumberPicker picker,int oldVal, int newVal){
                //Display the newly selected number from picker
                tv.setText("Selected Number : " + newVal);
                numb2 = newVal;
            }
        });



        proximityContentManager = new ProximityContentManager(this,//checks to see if the user is near a beacon
                Arrays.asList(
                        // TODO: replace with UUIDs, majors and minors of your own beacons
                        new BeaconID("B9407F30-F5F8-466E-AFF9-25556B57FE6D", 13137, 13952)),
                new EstimoteCloudBeaconDetailsFactory());

        final BeaconNotificationsManager beaconNotificationsManager = new BeaconNotificationsManager(this);//notifies the user
        beaconNotificationsManager.addNotification(new BeaconID(
                        "B9407F30-F5F8-466E-AFF9-25556B57FE6D", 13137, 13952),
                "You are connected now!", "You are no longer connected");

        proximityContentManager.setListener(new ProximityContentManager.Listener() {
            @Override
            public void onContentChanged(Object content) {//used to change the text and colour of background when connected
                String text;
                Integer backgroundColor;

                if (content != null) {//check to see if the beacon is in range.
                    EstimoteCloudBeaconDetails beaconDetails = (EstimoteCloudBeaconDetails) content;
                    text = "You're in " + beaconDetails.getBeaconName() + "'s range!";
                    backgroundColor = BACKGROUND_COLORS.get(beaconDetails.getBeaconColor());


                } else {//if the beacon is not in range
                    text = "No beacons in range.";
                    backgroundColor = null;
                }
                beaconNotificationsManager.startMonitoring();//monitor in background for beacon
                ((TextView) findViewById(R.id.textView)).setText(text);//set the text to be in range or not
                findViewById(R.id.relativeLayout).setBackgroundColor(//change colour
                        backgroundColor != null ? backgroundColor : BACKGROUND_COLOR_NEUTRAL);
            }
        });


    }

    @Override
    protected void onResume() {//when resuming the program
        super.onResume();

        if (!SystemRequirementsChecker.checkWithDefaultDialogs(this)) {
            Log.e(TAG, "Can't scan for beacons, some pre-conditions were not met");
            Log.e(TAG, "Read more about what's required at: http://estimote.github.io/Android-SDK/JavaDocs/com/estimote/sdk/SystemRequirementsChecker.html");
            Log.e(TAG, "If this is fixable, you should see a popup on the app's screen right now, asking to enable what's necessary");
        } else {
            Log.d(TAG, "Starting ProximityContentManager content updates");
            proximityContentManager.startContentUpdates();
        }
    }

    @Override
    protected void onPause() {//on pausing the program
        super.onPause();
        Log.d(TAG, "Stopping ProximityContentManager content updates");
        proximityContentManager.stopContentUpdates();
    }

    @Override
    protected void onDestroy() {//on killing the program
        super.onDestroy();
        proximityContentManager.destroy();

    }
}
