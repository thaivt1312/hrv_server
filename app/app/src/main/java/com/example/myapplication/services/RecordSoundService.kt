package com.example.myapplication.services

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Handler
import android.os.Looper
import android.util.Log
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.myapplication.firebase.MyFirebaseInstanceIDService
import com.example.myapplication.utils.data.GSonRequest
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.tasks.CancellationTokenSource
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

class RecordSoundService(context: Context, params: WorkerParameters) : Worker(context, params) {

    private lateinit var audioRecord: AudioRecord
    private var isRecording = false
    private val sampleRate = 16000
    private val channelConfig = AudioFormat.CHANNEL_IN_MONO
    private val audioFormat = AudioFormat.ENCODING_PCM_16BIT
    private val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat)
    private val audioData = ByteArray(bufferSize)

    private val LOG_TAG = "AudioRecordTest"
    private val inputFile = "${applicationContext.externalCacheDir?.absolutePath}/audio.pcm"
    private val outputFile = "${applicationContext.externalCacheDir?.absolutePath}/audio.wav"

    private val RECORD_TIME: Long = 10000

    override fun onStopped() {
        // Cleanup because you are being stopped.
        Log.d(LOG_TAG, "stop recording")
    }

    override fun doWork(): Result {

        startRecording()
        return Result.success()
    }

    @SuppressLint("MissingPermission")
    private fun startRecording() {
        audioRecord = AudioRecord(
            MediaRecorder.AudioSource.MIC,
            sampleRate,
            channelConfig,
            audioFormat,
            bufferSize
        )

        audioRecord.startRecording()
        isRecording = true

        val out = File(inputFile)
        val outputStream = FileOutputStream(out)

        Log.d(LOG_TAG, "start recording...")
        Thread {
            while (isRecording) {
                val read = audioRecord.read(audioData, 0, bufferSize)
                if (read > 0) {
                    outputStream.write(audioData, 0, read)
                }
            }
            outputStream.close()
        }.start()

        // Stop recording after 10 seconds
        Handler(Looper.getMainLooper()).postDelayed({
            stopRecording()
        }, RECORD_TIME)
    }

    @SuppressLint("RestrictedApi", "MissingPermission")
    fun sendData() {

        val locationClient = LocationServices.getFusedLocationProviderClient(this.applicationContext)

        val priority = Priority.PRIORITY_HIGH_ACCURACY
        locationClient.getCurrentLocation(
            priority,
            CancellationTokenSource().token,
        )
            .addOnSuccessListener { location: Location? ->
                run {
                    val locationInfo =
                        "Current location is \n" + "lat : ${location?.latitude}\n" +
                                "long : ${location?.longitude}\n" + "fetched at ${System.currentTimeMillis()}"
                    Log.d("Location", locationInfo)


                    FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
                        if (!task.isSuccessful) {
                            Log.w(MyFirebaseInstanceIDService.TAG, "Fetching FCM registration token failed", task.exception)
                            return@OnCompleteListener
                        }

                        // Get new FCM registration token
                        val token = task.result

                        Log.i("info message", "Making post api...")

                        val gsonRequest = GSonRequest()
                        val file = File(outputFile)
//            val MEDIA_TYPE_MARKDOWN = "text/x-markdown; charset=utf-8".toMediaType()
                        val requestBody: RequestBody = MultipartBody.Builder()
                            .setType(MultipartBody.FORM)
                            .addFormDataPart("file",
                                "file.wav",
                                file.asRequestBody("media/type".toMediaTypeOrNull())
                            )
                            .addFormDataPart("latitude", location?.latitude.toString())
                            .addFormDataPart("longitude", location?.longitude.toString())
                            .addFormDataPart("firebaseToken", token)
                            .build()

                        gsonRequest.callPostAPI("/post/record/", requestBody)

                        this.stop(0)

                    })

                }
            }

    }

    @SuppressLint("RestrictedApi")
    private fun stopRecording() {
        if (isRecording) {
            Log.d(LOG_TAG, "stop recording...")
            isRecording = false
            audioRecord.stop()
            audioRecord.release()
            convertPcmToWav(File(inputFile), File(outputFile))
            sendData()
        }
    }

    private fun convertPcmToWav(pcmFile: File, wavFile: File) {
        val channels = 1
        val bitDepth = 16
        val byteRate = sampleRate * channels * bitDepth / 8
        val pcmData = pcmFile.readBytes()

        val wavHeader = ByteArray(44)
        val totalDataLen = pcmData.size + 36
        val totalAudioLen = pcmData.size

        wavHeader[0] = 'R'.code.toByte()
        wavHeader[1] = 'I'.code.toByte()
        wavHeader[2] = 'F'.code.toByte()
        wavHeader[3] = 'F'.code.toByte()
        wavHeader[4] = (totalDataLen and 0xff).toByte()
        wavHeader[5] = (totalDataLen shr 8 and 0xff).toByte()
        wavHeader[6] = (totalDataLen shr 16 and 0xff).toByte()
        wavHeader[7] = (totalDataLen shr 24 and 0xff).toByte()
        wavHeader[8] = 'W'.code.toByte()
        wavHeader[9] = 'A'.code.toByte()
        wavHeader[10] = 'V'.code.toByte()
        wavHeader[11] = 'E'.code.toByte()
        wavHeader[12] = 'f'.code.toByte()
        wavHeader[13] = 'm'.code.toByte()
        wavHeader[14] = 't'.code.toByte()
        wavHeader[15] = ' '.code.toByte()
        wavHeader[16] = 16
        wavHeader[17] = 0
        wavHeader[18] = 0
        wavHeader[19] = 0
        wavHeader[20] = 1
        wavHeader[21] = 0
        wavHeader[22] = channels.toByte()
        wavHeader[23] = 0
        wavHeader[24] = (sampleRate and 0xff).toByte()
        wavHeader[25] = (sampleRate shr 8 and 0xff).toByte()
        wavHeader[26] = (sampleRate shr 16 and 0xff).toByte()
        wavHeader[27] = (sampleRate shr 24 and 0xff).toByte()
        wavHeader[28] = (byteRate and 0xff).toByte()
        wavHeader[29] = (byteRate shr 8 and 0xff).toByte()
        wavHeader[30] = (byteRate shr 16 and 0xff).toByte()
        wavHeader[31] = (byteRate shr 24 and 0xff).toByte()
        wavHeader[32] = (channels * bitDepth / 8).toByte()
        wavHeader[33] = 0
        wavHeader[34] = bitDepth.toByte()
        wavHeader[35] = 0
        wavHeader[36] = 'd'.code.toByte()
        wavHeader[37] = 'a'.code.toByte()
        wavHeader[38] = 't'.code.toByte()
        wavHeader[39] = 'a'.code.toByte()
        wavHeader[40] = (totalAudioLen and 0xff).toByte()
        wavHeader[41] = (totalAudioLen shr 8 and 0xff).toByte()
        wavHeader[42] = (totalAudioLen shr 16 and 0xff).toByte()
        wavHeader[43] = (totalAudioLen shr 24 and 0xff).toByte()

        val wavOutputStream = FileOutputStream(wavFile)
        wavOutputStream.write(wavHeader)
        wavOutputStream.write(pcmData)
        wavOutputStream.close()
    }

}