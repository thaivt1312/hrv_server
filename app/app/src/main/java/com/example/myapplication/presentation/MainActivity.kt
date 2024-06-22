/* While this template provides a good starting point for using Wear Compose, you can always
 * take a look at https://github.com/android/wear-os-samples/tree/main/ComposeStarter and
 * https://github.com/android/wear-os-samples/tree/main/ComposeAdvanced to find the most up to date
 * changes to the libraries and their usages.
 */

package com.example.myapplication.presentation

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View.OnClickListener
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import androidx.activity.ComponentActivity
import androidx.annotation.RequiresApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.core.app.ActivityCompat.requestPermissions
import androidx.core.content.ContextCompat
import androidx.wear.compose.material.MaterialTheme
import androidx.wear.compose.material.Text
import com.example.myapplication.R
import com.example.myapplication.presentation.theme.MyApplicationTheme
import com.example.myapplication.utils.data.CheckDeviceResponse
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging
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


class MainActivity : ComponentActivity() {

    private val TAG = "____Main___"
    var hasSensorPermission = false
    var hasRecordPermission = false
    var hasCoastLocationPermission = false
    var hasFineLocationPermission = false
    var loggedIn = false

    @SuppressLint("HardwareIds")
    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        hasSensorPermission = checkPermission(Manifest.permission.BODY_SENSORS)
        hasRecordPermission = checkPermission(Manifest.permission.RECORD_AUDIO)
        hasCoastLocationPermission = checkPermission(Manifest.permission.ACCESS_COARSE_LOCATION)
        hasFineLocationPermission = checkPermission(Manifest.permission.ACCESS_FINE_LOCATION)
        if (hasSensorPermission && hasRecordPermission && hasCoastLocationPermission && hasFineLocationPermission) {
            checkDevice(Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID))
        }
        val sensorButton = CustomButton(this, Manifest.permission.BODY_SENSORS, 1001)
        val recordButton = CustomButton(this, Manifest.permission.RECORD_AUDIO, 1002)
        val coastLocationButton = CustomButton(this, Manifest.permission.ACCESS_COARSE_LOCATION, 1003)
        val fineLocationButton = CustomButton(this, Manifest.permission.ACCESS_FINE_LOCATION, 1004)
        val logoutButton = LogoutButton(this)
        val ll = LinearLayout(this).apply {
            addView(sensorButton,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    75,
                    0f))
            addView(recordButton,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    75,
                    0f))
            addView(coastLocationButton,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    75,
                    0f))
            addView(fineLocationButton,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    75,
                    0f))
            addView(logoutButton,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    75,
                    0f))
        }
        ll.orientation = LinearLayout.VERTICAL
        ll.setPadding(20, 20, 20, 20)
        setContentView(ll)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
    }

    @SuppressLint("HardwareIds")
    private fun checkPermission(permission: String): Boolean { // step 3 started (according to content detail)

        // Runtime permission ------------
        // Permission has not been granted, so request it
        return ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED
    }

    private fun requestPermission(permission: String, requestCode: Int) {
        requestPermissions(
            this,
            arrayOf(permission),
            requestCode
        )
    }


    private fun checkDevice(androidId: String) {
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(OnCompleteListener<String?> { task ->
                if (!task.isSuccessful) {
                    Log.w(TAG, "FCM registration token failed", task.exception)
                    return@OnCompleteListener
                }

                // Get new FCM registration token
                val token = task.result

                // Log and toast
                val firebaseToken = token
                Log.d(TAG, firebaseToken)

                val apiBaseUrl = "https://intent-alien-crisp.ngrok-free.app/api"
                val client = OkHttpClient()

                val moshi = Moshi.Builder()
                    .addLast(KotlinJsonAdapterFactory()).build()

                val jsonAdapter: JsonAdapter<CheckDeviceResponse> =
                    moshi.adapter(CheckDeviceResponse::class.java)
                Log.d("ANDROID_ID", androidId)
                val formBody = FormBody.Builder()
                formBody.add("deviceId", androidId)
                formBody.add("firebaseToken", firebaseToken.toString())
                val body: FormBody = formBody.build()

                val request = Request.Builder()
                    .url("$apiBaseUrl/login/checkDevice/")
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
                            if (check != null) {
                                loggedIn = (check == "true")
                                print(check)
                            }
                        }
                    }
                })
            })
    }

    private fun logout(androidId: String) {
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(OnCompleteListener<String?> { task ->
                if (!task.isSuccessful) {
                    Log.w(TAG, "FCM registration token failed", task.exception)
                    return@OnCompleteListener
                }

                // Get new FCM registration token
                val token = task.result

                // Log and toast
                val firebaseToken = token
                Log.d(TAG, firebaseToken)

                val apiBaseUrl = "https://intent-alien-crisp.ngrok-free.app/api"
                val client = OkHttpClient()

                val moshi = Moshi.Builder()
                    .addLast(KotlinJsonAdapterFactory()).build()

                val jsonAdapter: JsonAdapter<CheckDeviceResponse> =
                    moshi.adapter(CheckDeviceResponse::class.java)
                Log.d("ANDROID_ID", androidId)
                val formBody = FormBody.Builder()
                formBody.add("deviceId", androidId)
                formBody.add("firebaseToken", firebaseToken.toString())
                val body: FormBody = formBody.build()

                val request = Request.Builder()
                    .url("$apiBaseUrl/login/checkDevice/")
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
                            if (check != null) {
                                print(check)
                            }
                        }
                    }
                })
            })

    }

    @SuppressLint("HardwareIds")
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            // Permission granted
            if (requestCode == 1001) {
                this.hasSensorPermission = true
            } else if (requestCode == 1002) {
                this.hasRecordPermission = true
            } else if (requestCode == 1003) {
                this.hasCoastLocationPermission = true
            }else if (requestCode == 1004) {
                this.hasFineLocationPermission = true
            }
            if (hasSensorPermission && hasRecordPermission && hasCoastLocationPermission && hasFineLocationPermission) {
                checkDevice(Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID))
            }
        } else {

        }
    }

//    @SuppressLint("AppCompatCustomView")
    internal inner class CustomButton(ctx: Context, permission: String, requestCode: Int)
        : Button(ctx) {

        private var clicker: OnClickListener = OnClickListener {
            val hasPermission = when(requestCode) {
                1001 -> hasSensorPermission
                1002 -> hasRecordPermission
                1003 -> hasCoastLocationPermission
                1004 -> hasFineLocationPermission
                else -> {false}
            }
            if (!hasPermission) {
                requestPermission(permission, requestCode)
            }
            text = when (hasPermission) {
                true -> "Has permission"
                false -> "Request permission"
            }
        }
        init {
            text = "Check permission"
            textSize = 8F
            setPadding(2, 2, 2, 2)
            setOnClickListener(clicker)
        }
    }

    internal inner class LogoutButton(ctx: Context)
        : Button(ctx) {

        @SuppressLint("HardwareIds")
        private var clicker: OnClickListener = OnClickListener {
            val deviceId = Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID)
            if (loggedIn) {
//                logout(deviceId)
            } else {
                checkDevice(deviceId)
            }
            text = when (loggedIn) {
                true -> "Log out"
                false -> "Log in"
            }
        }
        init {
            text = "Log in"
            textSize = 8F
            setOnClickListener(clicker)
        }
    }

}

@Composable
fun WearApp(greetingName: String) {
    MyApplicationTheme {
        /* If you have enough items in your list, use [ScalingLazyColumn] which is an optimized
         * version of LazyColumn for wear devices with some added features. For more information,
         * see d.android.com/wear/compose.
         */
        Row {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colors.background),
                verticalArrangement = Arrangement.Center
            ) {
                Greeting(greetingName = greetingName)
            }
        }
    }
}

@Composable
fun Greeting(greetingName: String) {
    Text(
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            color = MaterialTheme.colors.primary,
            text = stringResource(R.string.hello_world, greetingName)
    )
}

@Preview(device = Devices.WEAR_OS_SMALL_ROUND, showSystemUi = true)
@Composable
fun DefaultPreview() {
    WearApp("Preview Android")
}