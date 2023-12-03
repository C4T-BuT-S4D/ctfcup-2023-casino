package ru.ctfcup.c4tpixx

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import coil.compose.AsyncImage
import coil.decode.ImageDecoderDecoder
import coil.request.ImageRequest
import ru.ctfcup.c4tpixx.ui.theme.C4TPixxTheme
import ru.ctfcup.c4tpixx.ui.theme.nablaFontFamily


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            C4TPixxTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Welcome to")
                            Text(
                                "C4T pixx",
                                fontFamily = nablaFontFamily,
                                fontSize = 48.sp,
                                color = MaterialTheme.colorScheme.primary
                            )
                            Spacer(Modifier.height(48.dp))

                            var secretDialogShown by remember { mutableStateOf(false) }

                            PixxGallery(onSecretLongTap = { secretDialogShown = true })

                            if (secretDialogShown) {
                                SecretInputDialog(
                                    onDismissRequest = { secretDialogShown = false },
                                    onSecretEntered = {
                                        secretDialogShown = false
                                        Log.d("Secret", "Secret entered: $it")
                                    }
                                )
                            }

                            Spacer(Modifier.height(24.dp))
                            Text("Find the secret!", color = MaterialTheme.colorScheme.secondary)
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SecretInputDialog(
    onDismissRequest: () -> Unit,
    onSecretEntered: (String) -> Unit,
) {
    var text by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = { onDismissRequest() },
        title = { Text("Alert dialog example") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                placeholder = { Text("Hello Compose") },
                singleLine = true
            )
        },
        confirmButton = {
            Button(
                onClick = {
                    if (text.isNotEmpty()) {
                        onSecretEntered(text)
                    }
                },
                enabled = text.isNotEmpty()
            ) {
                Text("Filled")
            }
        },
        dismissButton = {
            TextButton(onClick = { onDismissRequest() }) {
                Text("Text Button")
            }
        }
    )
}


@OptIn(ExperimentalFoundationApi::class)
@Composable
fun PixxGallery(onSecretLongTap: () -> Unit) {
    val context = LocalContext.current
    val gifs = context.assets.list("pixx")!!.map { "file:///android_asset/pixx/$it" }

    val state = rememberPagerState { gifs.size }
    HorizontalPager(
        state = state,
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(start = 16.dp, end = 16.dp)
    ) { page ->
        OutlinedCard(
            shape = RoundedCornerShape(16.dp),
            modifier = if ("holdme" in gifs[page]) {
                Modifier.combinedClickable(
                    onClick = { },
                    onLongClick = {
                        Log.d("PixxGallery", "Woah such long tap!")
                        onSecretLongTap()
                    }
                )
            } else {
                Modifier
            }
                .padding(horizontal = 4.dp)
        ) {
            AsyncGif(gifs[page])
        }
    }
}

@Composable
fun AsyncGif(path: String) {
    val imageRequest = ImageRequest.Builder(LocalContext.current)
        .data(path)
        .decoderFactory(ImageDecoderDecoder.Factory())
        .crossfade(true)
        .build()

    AsyncImage(
        modifier = Modifier
            .fillMaxWidth()
            .height(240.dp),
        model = imageRequest,
        contentDescription = null,
        onError = {
            Log.e("AsyncGif", it.result.throwable.message!!)
        }
    )
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
fun GreetingPreview() {
    C4TPixxTheme {
        Greeting("Android")
    }
}