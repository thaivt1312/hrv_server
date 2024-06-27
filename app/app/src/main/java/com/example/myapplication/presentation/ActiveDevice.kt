package com.example.myapplication.presentation

import android.annotation.SuppressLint
import android.graphics.drawable.ColorDrawable
import android.graphics.drawable.Drawable
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.R
import com.example.myapplication.presentation.ui.theme.MyApplicationTheme
import com.example.myapplication.utils.data.CheckDeviceResponse
import com.squareup.moshi.JsonAdapter
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.Call
import okhttp3.Callback
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.io.IOException


class ActiveDeviceActivity : ComponentActivity() {
    private lateinit var loginResult: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.active_device)

        val passcode: EditText = findViewById(R.id.passcode)

        passcode.text

        val informationText: TextView = findViewById(R.id.text_information)

        val sendButton: Button = findViewById(R.id.button_send)
        val background = sendButton.background as Drawable
        sendButton.setOnClickListener {
            Log.d("ACTIVE", "${passcode.text} ${(background as ColorDrawable).color}")
            informationText.setText("Testing")
        }

    }

//    @OptIn(ExperimentalMaterial3Api::class)
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        setContent {
//            MyApplicationTheme {
//                // A surface container using the 'background' color from the theme
//                Surface(
//                    modifier = Modifier.fillMaxSize(),
//                    color = MaterialTheme.colorScheme.background
//                ) {
//                    if (::loginResult.isInitialized && loginResult == "Login") {
//                        Greeting2(loginResult)
//                    }
//                    else {
//                        Column(
//                            modifier = Modifier.fillMaxSize(),
//                            verticalArrangement = Arrangement.Center,
//                            horizontalAlignment = Alignment.CenterHorizontally
//                        ) {
//                            var passcode by remember {
//                                mutableStateOf("")
//                            }
//                            TextField(
//                                value = passcode,
//                                onValueChange = {
//                                    passcode = it
////                                println(passcode)
//                                },
//                                label = {
//                                    Text(text = "Passcode")
//                                }
//                            )
//                            println(passcode)
//                            Button(onClick = {
//                                handleLogin(passcode)
//                            }) {
//
//                            }
//                        }
//                    }
//                }
//            }
//        }
//    }

    @SuppressLint("HardwareIds")
    fun handleLogin(passcode: String) {
        val androidId = Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID);
        val apiBaseUrl = "https://intent-alien-crisp.ngrok-free.app/api"
        val client = OkHttpClient()

        val moshi = Moshi.Builder()
            .addLast(KotlinJsonAdapterFactory()).build()
        //    val type = Types.newParameterizedType(CheckDeviceResponse::class.java, CheckDeviceResponse::class.java)
        val jsonAdapter: JsonAdapter<CheckDeviceResponse> = moshi.adapter(CheckDeviceResponse::class.java)
//        val androidId = MyFirebaseInstanceIDService.androidId
        Log.d("ANDROID_ID", androidId)
        val formBody = FormBody.Builder()
        formBody.add("deviceId", androidId)
        formBody.add("passcode", passcode)
        val body: FormBody = formBody.build()
//        callPostAPI("/login/checkDevice/", body)

        val request = Request.Builder()
            .url("$apiBaseUrl/login/")
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful) throw IOException("Unexpected code $response")

                    val annotationData = jsonAdapter.fromJson(response.body.string())
                    val check = annotationData?.login
                    if(check == "started") {
                        loginResult = "login"
                        println(annotationData?.login)
                    }
                    else {
                        loginResult = ""
//                        intent = Intent(this@MainActivity, LoginActivity::class.java)
//                        startActivity(intent)
//                        finish()
                    }
                }
            }
        })
    }
}

@Composable
fun Greeting2(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyApplicationTheme {
        Greeting2("Android")
    }
}