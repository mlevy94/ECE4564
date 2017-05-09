package com.example.thayne.ece4564_app;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;

/**
 * Created by Thayne on 5/8/2017.
 */

public class RequestBuilder {

    //Login request body
    public static RequestBody PostBody(String user, String uuid, String height) {
        return new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("User", user)
                .addFormDataPart("UUID", uuid)
                .addFormDataPart("Height", height)
                .build();
    }


}

