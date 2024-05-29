package com.example.myapplication.utils.data

import com.google.gson.Gson
import android.util.Log
import com.example.myapplication.firebase.MyFirebaseInstanceIDService
import com.squareup.moshi.JsonAdapter
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.Call
import okhttp3.Callback
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.Response
import okhttp3.ResponseBody
import java.io.IOException


class GSonRequest {
    private val apiBaseUrl = "https://intent-alien-crisp.ngrok-free.app/api"
    private val client = OkHttpClient()
    private val name: String = ""
    val gson = Gson()

    val moshi = Moshi.Builder()
        .addLast(KotlinJsonAdapterFactory()).build()

    private fun makeCall(request: Request) {

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful) throw IOException("Unexpected code $response")

                    val json: String = gson.toJson(response.body?.string())
                    println(json)
                }
            }
        })
    }

    fun callGetAPI(apiUrl: String): Unit {
        val request = Request.Builder()
            .url(apiBaseUrl + apiUrl)
            .build()

        makeCall(request)
    }

    fun callPostAPI(apiUrl: String, requestBody: RequestBody): Unit {
        val request = Request.Builder()
            .url(apiBaseUrl + apiUrl)
            .post(requestBody)
            .build()

        makeCall(request)
    }

    fun login(passcode: String, androidId: String) {
//        val androidId = MyFirebaseInstanceIDService.androidId
        val token = MyFirebaseInstanceIDService.firebaseToken
        val formBody = FormBody.Builder()
        formBody.add("deviceId", androidId)
        formBody.add("firebaseToken", token)
        formBody.add("passcord", passcode)
        val body: FormBody = formBody.build()
        callPostAPI("/login/", body)
    }

    fun checkDevice(androidId: String, firebaseToken: String):String {
//        val androidId = MyFirebaseInstanceIDService.androidId
        Log.d("ANDROID_ID", androidId)
        val formBody = FormBody.Builder()
        formBody.add("deviceId", androidId)
        formBody.add("firebaseToken", firebaseToken)
        val body: FormBody = formBody.build()
//        callPostAPI("/login/checkDevice/", body)

        val request = Request.Builder()
            .url("$apiBaseUrl/login/checkDevice/")
            .post(body)
            .build()

        val moshi = Moshi.Builder()
            .addLast(KotlinJsonAdapterFactory()).build()
        //    val type = Types.newParameterizedType(CheckDeviceResponse::class.java, CheckDeviceResponse::class.java)
        val jsonAdapter: JsonAdapter<CheckDeviceResponse> = moshi.adapter(CheckDeviceResponse::class.java)
        var outCheck: String = ""
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Unexpected code $response")

            val annotationData = jsonAdapter.fromJson(response.body.string())
            println(response.body!!.string())
            val check = annotationData?.login
            if (check != null) {
                outCheck = check
            }

        }

        return outCheck

    }

}