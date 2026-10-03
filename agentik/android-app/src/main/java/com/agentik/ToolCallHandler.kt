package com.agentik

import com.squareup.okhttp3.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject

object ToolCallHandler {
    private val client = OkHttpClient.Builder()
        .addInterceptor(
            HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }
        )
        .build()

    private const val OMNIRoute_URL = "https://omni-route-agentik.on.tailscale.io/v1/chat/completions"
    private const val API_KEY = "YOUR_API_KEY_HERE"

    data class ToolCall(val name: String, val arguments: Map<String, Any>)

    suspend fun executeTool(toolCall: ToolCall): String = withContext(Dispatchers.IO) {
        val json = JSONObject().apply {
            put("model", "agentik-windows-control")
            put("messages", JSONObject().put("role", "user").put("content", "Execute: ${toolCall.name}"))
            put("tools", JSONObject().put("type", "function").put("function", JSONObject().put("name", toolCall.name)))
        }

        val request = Request.Builder()
            .url(OMNIRoute_URL)
            .post(RequestBody.create(MediaType.parse("application/json"), json.toString()))
            .addHeader("Authorization", "Bearer $API_KEY")
            .build()

        val response = client.newCall(request).execute()
        val body = response.body?.string() ?: return@withContext "Error: no response"
        JSONObject(body).getString("result")
    }
}
