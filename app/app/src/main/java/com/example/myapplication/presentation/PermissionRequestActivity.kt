package com.example.myapplication.presentation

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import androidx.activity.ComponentActivity
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.core.app.ActivityCompat
import com.example.myapplication.R
import com.example.myapplication.presentation.ui.theme.MyApplicationTheme


class PermissionRequestActivity : ComponentActivity() {
    private var hasSensorPermission = false
    private var hasRecordPermission = false
    private var hasCoastLocationPermission = false
    private var hasFineLocationPermission = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.permission_request)

        val button1: Button = findViewById(R.id.button1)
        button1.setOnClickListener {
            if (!hasSensorPermission) {
                requestPermission(Manifest.permission.BODY_SENSORS, 1001)
            }
        }

        val button2: Button = findViewById(R.id.button2)
        button2.setOnClickListener {
            if (!hasRecordPermission) {
                requestPermission(Manifest.permission.RECORD_AUDIO, 1002)
            }
        }

        val button3: Button = findViewById(R.id.button3)
        button3.setOnClickListener {
            if (!hasCoastLocationPermission) {
                requestPermission(Manifest.permission.ACCESS_COARSE_LOCATION, 1003)
            }
        }

        val button4: Button = findViewById(R.id.button4)
        button4.setOnClickListener {
            if (!hasFineLocationPermission) {
                requestPermission(Manifest.permission.ACCESS_FINE_LOCATION, 1004)
            }
        }
    }

    private fun requestPermission(permission: String, requestCode: Int) {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(permission),
            requestCode
        )
    }
    @SuppressLint("HardwareIds", "WearRecents")
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
//                checkDevice(Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID))
                val myIntent = Intent(this, MainActivity::class.java)
                myIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
                finishAffinity()
                startActivity(myIntent)
            }
        }
    }

}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview2() {
    MyApplicationTheme {
        Greeting("Android")
    }
}