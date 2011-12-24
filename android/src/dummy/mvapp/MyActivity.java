package dummy.mvapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;
import dummy.mvapp.search.ResultsActivity;
import org.apache.commons.io.IOUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.util.EntityUtils;
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

    public void Scan3442367263(View view) throws Exception  {
        Intent myIntent = new Intent(this, ResultsActivity.class);
        this.startActivity(myIntent);
    }

    public void JsonApi(View view) throws Exception  {

        DefaultHttpClient httpclient = new DefaultHttpClient();
        try {
            httpclient.getCredentialsProvider().setCredentials(
                    new AuthScope("192.168.120.24", 5000),
                    new UsernamePasswordCredentials("a", "a"));

            HttpGet httpget = new HttpGet("http://192.168.120.24:5000/JsonApi/isbn?q=3442367263");

            Log.d(TAG, "executing request" + httpget.getRequestLine());
            HttpResponse response = httpclient.execute(httpget);
            Log.d(TAG, "response.getStatusLine(): " + response.getStatusLine());

            HttpEntity entity = response.getEntity();
//            String theString = IOUtils.toString(new URI("http://192.168.120.24:5000/JsonApi/isbn?q=3442367263"));
            String theString = IOUtils.toString(entity.getContent());
            Log.d(TAG, "theString: " + theString);

            JSONObject result = new JSONObject(theString);
            Log.d(TAG, "isbn: " + result.getString("isbn"));
            JSONArray media = result.getJSONArray("media");
            for (int i=0; i< media.length(); i++) {
                JSONObject medium = media.getJSONObject(i);
                Log.d(TAG, medium.getString("title"));
            }
//            EntityUtils.consume(entity);
        } finally {
            // When HttpClient instance is no longer needed,
            // shut down the connection manager to ensure
            // immediate deallocation of all system resources
            httpclient.getConnectionManager().shutdown();
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
