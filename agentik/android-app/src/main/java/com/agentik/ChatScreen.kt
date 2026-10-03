package com.agentik

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agentik.ui.theme.AgentikTheme

data class ChatMessage(val text: String, val isUser: Boolean)

class ChatScreen : ComponentActivity() {
    private val messages = mutableStateListOf<ChatMessage>()
    private var inputText by remember { mutableStateOf("") }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AgentikTheme {
                Scaffold(
                    topBar = {
                        CenterAlignedTopAppBar(title = { Text("Agentik") })
                    }
                ) { padding ->
                    Column(modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)) {
                        MessageList(messages)
                        Spacer(modifier = Modifier.height(8.dp))
                        ChatInputField(
                            onValueChange = { inputText = it },
                            onSend = { sendMessage() }
                        )
                    }
                }
            }
        }
    }

    private fun sendMessage() {
        if (inputText.isNotBlank()) {
            messages.add(ChatMessage(inputText, true))
            inputText = ""
            // TODO: Send to OmniRoute and handle response
        }
    }

    @Composable
    private fun MessageList(messages: List<ChatMessage>) {
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            items(messages) { message ->
                MessageBubble(message.text, message.isUser)
            }
        }
    }

    @Composable
    private fun MessageBubble(text: String, isUser: Boolean) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
        ) {
            Text(
                text = text,
                modifier = Modifier
                    .padding(16.dp)
                    .background(
                        if (isUser) Color(0xFF6200EE) else Color(0xFFE0E0E0),
                        RoundedCornerShape(16.dp)
                    )
                    .padding(8.dp)
                    .wrapContentWidth(align = Alignment.End),
                color = if (isUser) Color.White else Color.Black,
                textAlign = TextAlign.Start
            )
        }
    }

    @Composable
    private fun ChatInputField(
        onValueChange: (String) -> Unit,
        onSend: () -> Unit
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
        ) {
            OutlinedTextField(
                value = inputText,
                onValueChange = onValueChange,
                label = { Text("Type a command...") },
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.width(8.dp))
            IconButton(onClick = onSend) {
                Icon(
                    imageVector = Icons.Default.Send,
                    contentDescription = "Send"
                )
            }
        }
    }
}