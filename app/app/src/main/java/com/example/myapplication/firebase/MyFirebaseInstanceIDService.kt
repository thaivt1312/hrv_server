package com.example.myapplication.firebase

import android.annotation.SuppressLint
import android.util.Log
import androidx.work.BackoffPolicy
import androidx.work.Constraints
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequest
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import com.example.myapplication.services.ReadHRService
import com.example.myapplication.services.RecordSoundService
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import java.util.concurrent.TimeUnit


class MyFirebaseInstanceIDService : FirebaseMessagingService() {
    companion object{
        const val TAG = "PUSH_Android"
        lateinit var firebaseToken: String

    }

    @SuppressLint("HardwareIds")
    override fun onNewToken(token: String) {
        Log.d(TAG, "Refreshed token: $token")

        val sharedPreferences = getSharedPreferences("file_save_token", MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.putString("myToken", token)
        editor.apply()
        firebaseToken = token

    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {

        // TODO(developer): Handle FCM messages here.
        // Not getting messages here? See why this may be: https://goo.gl/39bRNJ
        Log.d(TAG, "From: " + remoteMessage.from)
        print("From: " + remoteMessage.from)

        // Check if message contains a data payload.
        if (remoteMessage.data.size > 0) {
            Log.d(TAG, "Message data payload: " + remoteMessage.data["data"])

            if ( /* Check if data needs to be processed by long running job */true) {
                val constraints: Constraints = Constraints.Builder().apply {
                    setRequiredNetworkType(NetworkType.CONNECTED)
                }.build()
                val msg = remoteMessage.data["data"]
                if (msg == "getHRData") {
                    val request: OneTimeWorkRequest =
                        // Tell which work to execute
                        OneTimeWorkRequestBuilder<ReadHRService>()
                            // Sets the input data for the ListenableWorker
//                        .setInputData(input)
                            // If you want to delay the start of work by 60 seconds
                            .setInitialDelay(1, TimeUnit.SECONDS)
                            // Set a backoff criteria to be used when retry-ing
                            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30000, TimeUnit.MILLISECONDS)
                            // Set additional constraints
                            .setConstraints(constraints)
                            .build()
                    WorkManager.getInstance(this)
                        .enqueueUniqueWork("hr-monitor-worker", ExistingWorkPolicy.REPLACE, request)
                }
                else if (msg == "getRecord") {
                    val request: OneTimeWorkRequest =
                        // Tell which work to execute
                        OneTimeWorkRequestBuilder<RecordSoundService>()
                            // Sets the input data for the ListenableWorker
//                        .setInputData(input)
                            // If you want to delay the start of work by 60 seconds
                            .setInitialDelay(1, TimeUnit.SECONDS)
                            // Set a backoff criteria to be used when retry-ing
                            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30000, TimeUnit.MILLISECONDS)
                            // Set additional constraints
                            .setConstraints(constraints)
                            .build()
                    WorkManager.getInstance(this)
                        .enqueueUniqueWork("record-audio-worker", ExistingWorkPolicy.REPLACE, request)

                }
                // For long-running tasks (10 seconds or more) use Firebase Job Dispatcher.

            } else {
                // Handle message within 10 seconds
//                handleNow()
            }
        }

        // Check if message contains a notification payload.
        if (remoteMessage.notification != null) {
            //This line will print out push message which we will send from our server
            Log.d(TAG,"Message Notification Body: " + remoteMessage.notification!!.body
            )
        }

        // Also if you intend on generating your own notifications as a result of a received FCM
        // message, here is where that should be initiated. See sendNotification method below.
    }

}