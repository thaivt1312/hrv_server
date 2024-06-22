package com.example.myapplication.utils.data

import com.google.gson.Gson
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.Response
import java.io.IOException

class GSonRequest {
    private val apiBaseUrl = "https://intent-alien-crisp.ngrok-free.app/api"
    private val client = OkHttpClient()
    val gson = Gson()

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

}