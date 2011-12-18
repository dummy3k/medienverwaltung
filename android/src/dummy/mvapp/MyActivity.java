package dummy.mvapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;
import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.net.URI;

public class MyActivity extends Activity
{
    private static final String TAG = "MyActivity";

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }

    public void api(View view) {
        //this.toast("ho");
        try{
            String theString = IOUtils.toString(new URI("http://192.168.120.24:5000/JsonApi/isbn?q=3442367263"));
            Log.d(TAG, "theString: " + theString);
            JSONObject result = new JSONObject(theString);
            Log.d(TAG, result.getString("isbn"));
            JSONArray media = result.getJSONArray("media");
            for (int i=0; i< media.length(); i++) {
                JSONObject medium = media.getJSONObject(i);
                Log.d(TAG, medium.getString("title"));
            }

        } catch (Exception ex) {
            this.toast(ex);
        }
            

    }

    private void toast(Exception ex) {
        Log.e(TAG, ex.toString());
        this.toast(ex.toString());
    }
    
    private void toast(String s) {
        Context context = getApplicationContext();
        CharSequence text = "Hello toast!";
        int duration = Toast.LENGTH_SHORT;

        Toast.makeText(context, s, duration).show();
    }
    
    public void selfDestruct(View view) {
        // Kabloey

        Intent intent = new Intent("com.google.zxing.client.android.SCAN");
        intent.setPackage("com.google.zxing.client.android");
        //intent.putExtra("SCAN_MODE", "QR_CODE_MODE");
        startActivityForResult(intent, 0);

    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (requestCode == 0) {
            if (resultCode == RESULT_OK) {
                String contents = intent.getStringExtra("SCAN_RESULT");
                String format = intent.getStringExtra("SCAN_RESULT_FORMAT");
                // Handle successful scan
                Context context = getApplicationContext();
                CharSequence text = "Hello toast!";
                int duration = Toast.LENGTH_SHORT;

                Toast.makeText(context, format, duration).show();
                Toast.makeText(context, contents, duration).show();
            } else if (resultCode == RESULT_CANCELED) {
                // Handle cancel
            }
        }
    }

}
