package com.agentik

import android.content.Context
import android.media.MediaRecorder
import android.os.Environment
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

/**
 * Voice Input handler using Needle 3 Whistle module.
 *
 * Note: Needle 3 Whistle is a native module (Python/C++).
 * For Android integration, use the Needle Android SDK or
 * wrap the native library via JNI / AAR.
 *
 * This stub records audio and returns a placeholder text
 * for development/testing purposes.
 */
class VoiceInput(private val context: Context) {

    private var mediaRecorder: MediaRecorder? = null
    private var outputFile: File? = null

    suspend fun startRecording(): File = withContext(Dispatchers.IO) {
        val dir = context.getExternalFilesDir(Environment.DIRECTORY_RECORDINGS)
            ?: throw IllegalStateException("Cannot access recordings directory")
        outputFile = File(dir, "voice_input_${System.currentTimeMillis()}.3gp")

        mediaRecorder = MediaRecorder().apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP)
            setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB)
            setOutputFile(outputFile!!.absolutePath)
            prepare()
            start()
        }
        outputFile!!
    }

    suspend fun stopRecording(): String = withContext(Dispatchers.IO) {
        mediaRecorder?.apply {
            stop()
            reset()
            release()
        }
        mediaRecorder = null

        // TODO: Replace with actual Needle 3 Whistle transcription.
        // For now, return a placeholder text.
        "Placeholder: voice input recorded at ${outputFile?.absolutePath}"
    }
}
