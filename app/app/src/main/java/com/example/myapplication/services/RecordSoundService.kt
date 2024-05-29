package com.example.myapplication.services

import android.annotation.SuppressLint
import android.content.Context
import android.media.AudioManager
import android.media.MediaRecorder
import android.os.Build
import android.os.PowerManager
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.myapplication.firebase.MyFirebaseInstanceIDService
import com.example.myapplication.utils.data.GSonRequest
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.IOException

class RecordSoundService(context: Context, params: WorkerParameters) : Worker(context, params),
    MediaRecorder.OnInfoListener {

    private val LOG_TAG = "AudioRecordTest"
    private var fileName: String = ""
    private var recorder: MediaRecorder? = null
    var audioManager: AudioManager? = null
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
        Log.d(LOG_TAG, "stop recording")
        releaseWakeLock()
    }

    override fun doWork(): Result {
        acquireWakeLock()
        audioManager = applicationContext.getSystemService(ComponentActivity.AUDIO_SERVICE) as AudioManager

        fileName = "${applicationContext.externalCacheDir?.absolutePath}/audiorecord.mp3"
//        checkPlaySoundPermission()
        startRecording()
        return Result.success()
    }

    private fun startRecording() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            recorder = MediaRecorder(applicationContext).apply {
                setAudioSource(MediaRecorder.AudioSource.MIC)
                setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
                setOutputFile(fileName)
                setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
                setMaxDuration(10000)

            }
        }
        recorder!!.setOnInfoListener { mr, what, extra ->
            if (what == MediaRecorder.MEDIA_RECORDER_INFO_MAX_DURATION_REACHED) {
//                recorder!!.stop()
                stopRecording()
            }
        }

        try {
            recorder!!.prepare()
        } catch (e: IOException) {
            Log.e(LOG_TAG, "prepare() failed")
        }

        Log.d(LOG_TAG, "start recording...")
        recorder!!.start()
    }

    @SuppressLint("RestrictedApi")
    fun sendData() {
        FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
            if (!task.isSuccessful) {
                Log.w(MyFirebaseInstanceIDService.TAG, "Fetching FCM registration token failed", task.exception)
                return@OnCompleteListener
            }

            // Get new FCM registration token
            val token = task.result

            Log.i("info message", "Making post api...")

            val gsonRequest = GSonRequest()
            val file = File("${applicationContext.externalCacheDir?.absolutePath}/audiorecord.mp3")
//            val MEDIA_TYPE_MARKDOWN = "text/x-markdown; charset=utf-8".toMediaType()
            val requestBody: RequestBody = MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file",
                    "file.mp3",
                    file.asRequestBody("media/type".toMediaTypeOrNull())
                )
                .addFormDataPart("firebaseToken", token)
                .build()

            gsonRequest.callPostAPI("/post/record/", requestBody)

            this.stop(0)

        })
    }

    @SuppressLint("RestrictedApi")
    private fun stopRecording() {
        Log.d(LOG_TAG, "stop recording...")

        recorder?.apply {
            stop()
            release()
        }
        recorder = null
        sendData()
    }

    override fun onInfo(mr: MediaRecorder?, what: Int, extra: Int) {
        if (what == MediaRecorder.MEDIA_RECORDER_INFO_MAX_DURATION_REACHED) {
            //display in long period of time
//            Toast.makeText(applicationContext, "End Recording", Toast.LENGTH_LONG).show()
            stopRecording()
        }
    }

}