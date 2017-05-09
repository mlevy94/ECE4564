package com.example.thayne.ece4564_app;

import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by Thayne on 5/8/2017.
 */

public class ApiCall {

    //POST network request
    public static String POST(OkHttpClient client, String url, RequestBody body) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }
}
