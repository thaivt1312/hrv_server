package com.example.myapplication.services

import android.annotation.SuppressLint
import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.location.Location
import android.os.PowerManager
import android.util.Log
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.myapplication.firebase.MyFirebaseInstanceIDService.Companion.TAG
import com.example.myapplication.utils.data.GSonRequest
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging
import com.google.gson.Gson
import okhttp3.FormBody


class ReadHRService(context: Context, params: WorkerParameters) : Worker(context, params)
    , SensorEventListener {

//    private val BODY_SENSORS_PERMISSION_CODE = 1001
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null
    private val mRRIntervals = mutableListOf<Double>()
    private val mRRIntervalsTime = mutableListOf<Long>()
    private val heartBeatArr = mutableListOf<Double>()
    private var mStartTime: Long = 0
    private var intervalCount: Long = 0
    private var running: Long = 0L

    private var RRIntervalNeed: Long = 10
    private var TimeLimit: Long = 30
    private var sensorType =
        Sensor.TYPE_HEART_RATE
//        69682

    private lateinit var wakeLock: PowerManager.WakeLock

    private fun acquireWakeLock() {
        val powerManager = applicationContext.getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AudioRecord::WakeLock")
        wakeLock.acquire(2*60*1000L /*2 minutes*/)
    }

    private fun releaseWakeLock() {
        if (wakeLock.isHeld) {
            wakeLock.release()
        }
    }

    override fun onStopped() {
        // Cleanup because you are being stopped.
        pauseHeartRateMonitoring()
        releaseWakeLock()
    }

    override fun doWork(): Result {
        acquireWakeLock()
        startHeartRateMonitoring()
        return Result.success()
    }

    private fun startHeartRateMonitoring() {
        sensorManager = this.applicationContext.getSystemService(Context.SENSOR_SERVICE) as SensorManager
        if (sensorManager.getDefaultSensor(sensorType) != null) {
            Log.d("Sensor Status:", "has heart beat sensor")
        } else {
            Log.d("Sensor Status:", "do not has heart beat sensor")
        }
        heartRateSensor = sensorManager.getDefaultSensor(sensorType)
        val sensorRegistered = sensorManager.registerListener(
            this,
            heartRateSensor,
            SensorManager.SENSOR_DELAY_FASTEST
        )
        Log.d("Sensor Status:", " Sensor registered: " + if (sensorRegistered) "yes" else "no")

        mStartTime = System.currentTimeMillis()
    }

    private fun pauseHeartRateMonitoring() {
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent) {
        if (event.sensor.type == sensorType) {
            val currentTimestamp = System.currentTimeMillis()
            val elapsedTime = currentTimestamp - mStartTime
            val heartRate = event.values[0]
            if (elapsedTime / 1000 > TimeLimit) {
                mStartTime = currentTimestamp
                sendData()
            }
            // Calculate R-R interval from heart rate (for demonstration purposes)
            if (intervalCount <= RRIntervalNeed) {
                val previousTimestamp: Long
                val rriTime : Long
                val rrInterval: Float
                if(mRRIntervalsTime.isNotEmpty()) {
                    previousTimestamp = mRRIntervalsTime.last()
                    rriTime = currentTimestamp - previousTimestamp
                    rrInterval = 60 * rriTime / heartRate
                }
                else {
                    rrInterval = 60 * elapsedTime / heartRate
                }
                running = elapsedTime
                Log.d( "heart rate","heart rate: $heartRate bpm")
                Log.d( "run","$elapsedTime ms: $rrInterval")
                if (heartRate > 10) {
                    mRRIntervals.add(rrInterval.toDouble())
                    heartBeatArr.add(heartRate.toDouble())
                    intervalCount++
                }
                mRRIntervalsTime.add(currentTimestamp)

            } else {
                mStartTime = currentTimestamp
                sendData()

            }
        }

    }

    @SuppressLint("RestrictedApi", "MissingPermission")
    fun sendData() {

        this.stop(0)
        val locationClient = LocationServices.getFusedLocationProviderClient(this.applicationContext)

        val priority = Priority.PRIORITY_HIGH_ACCURACY
        locationClient.getCurrentLocation(
            priority,
            CancellationTokenSource().token,
        )
            .addOnSuccessListener { location: Location? ->
                run {
                    var latitude: String
                    var longitude: String

                    if (location?.latitude == null) {
                        latitude = ""
                    } else {
                        latitude = location.latitude.toString()
                    }

                    if (location?.longitude == null) {
                        longitude = ""
                    } else {
                        longitude = location.longitude.toString()
                    }

                    val locationInfo =
                        "Current location is \n" + "lat : ${latitude}\n" +
                                "long : ${longitude}\n" + "fetched at ${System.currentTimeMillis()}"
                    Log.d("Location", locationInfo)
                    FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
                        if (!task.isSuccessful) {
                            Log.w(TAG, "Fetching FCM registration token failed", task.exception)
                            return@OnCompleteListener
                        }

                        // Get new FCM registration token
                        val token = task.result

                        Log.i("info message", "Making post api...")
                        val gsonRequest = GSonRequest()
                        val gson = Gson()
                        val arr: MutableList<Double> = mRRIntervals
                        val heartBeatData: MutableList<Double> = heartBeatArr
                        gson.toJson(arr.toString())
                        val formBody = FormBody.Builder()

                        formBody.add("firebaseToken", token!!)
                        formBody.add("hrData", arr.toString())
                        formBody.add("heartBeatData", heartBeatData.toString())
                        formBody.add("latitude", latitude)
                        formBody.add("longitude", longitude)
                        print(gson.toJson(arr.toString()))

                        val body: FormBody = formBody.build()
                        gsonRequest.callPostAPI("/post/hrData/", body)
                        mRRIntervals.clear()
                        mRRIntervalsTime.clear()
                        heartBeatArr.clear()
                        intervalCount = 0

                    })

                }
            }

    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Not used in this example
    }
}