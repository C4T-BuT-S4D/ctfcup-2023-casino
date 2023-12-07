package ru.ctfcup.flagboard

import android.content.Context
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.requiredHeight
import androidx.compose.foundation.layout.requiredWidth
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import ru.ctfcup.flagboard.ui.theme.FlagBoardTheme
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader
import java.security.MessageDigest
import java.util.Base64
import java.util.stream.Collectors
import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.DESedeKeySpec
import javax.crypto.spec.SecretKeySpec

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val game = Game(this)

        setContent {
            FlagBoardTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(horizontal = 12.dp),
                    color = MaterialTheme.colorScheme.background,
                ) {
                    val gameState by game.gameState.observeAsState()

                    Column(modifier = Modifier.fillMaxWidth()) {
                        Spacer(modifier = Modifier.height(20.dp))
                        Text("FlagBoard", style = MaterialTheme.typography.displayLarge)
                        Spacer(modifier = Modifier.weight(.5f))
                        Row(
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("now press ")
                            ExampleLetterButton(gameState!!.correctLetter)
                        }
                        Spacer(modifier = Modifier.weight(.2f))
                        Row(
                            horizontalArrangement = Arrangement.Center,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            UnfairKeyboard(gameState!!) { game.nextLevel() }
                        }
                        Spacer(modifier = Modifier.weight(.3f))
                    }
                }
            }
        }
    }
}


data class KeyboardLetter(
    val letter: String,
    val color: Color,
)


data class GameState(
    val displayedLetters: List<KeyboardLetter>,
    val correctLetter: KeyboardLetter,
    val rows: Int
)


class Game(context: Context) {
    private val levels = context.resources.openRawResource(R.raw.lookforme).lines()
    private var levelKey = ""

    private var currentLevel = 0
    private var maxLevel = levels.size

    private val colors =
        listOf(Color.Gray, Color.Red, Color.Green, Color.Blue, Color.Yellow, Color.Cyan)
    private val letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-"

    // Cache
    private val allKeyboardLetters = letters.flatMap { letter ->
        colors.map { color ->
            KeyboardLetter(letter.toString(), color)
        }
    }

    private val _gameState = MutableLiveData<GameState>()
    val gameState: LiveData<GameState> = _gameState

    init {
        nextLevel()
    }

    fun nextLevel() {
        if (currentLevel > maxLevel) {
            return
        }

        _gameState.value?.let { levelKey += it.correctLetter.letter }
        val leLetter = decrypt(levels[currentLevel], levelKey)
            .substring(currentLevel, currentLevel+1)

        currentLevel++
        if (currentLevel == 1) {
            val letter = allKeyboardLetters.find {
                it.letter == leLetter && it.color == Color.Gray
            }

            _gameState.value = GameState(
                displayedLetters = listOf(letter!!),
                correctLetter = letter,
                rows = 1
            )
        } else if (currentLevel <= 3) {
            val letter = allKeyboardLetters.find {
                it.letter == leLetter && it.color == Color.Gray
            }!!
            val otherLetters = allKeyboardLetters.filter {
                it != letter && it.color == Color.Gray
            }.shuffled().take(3)
            _gameState.value = GameState(
                displayedLetters = (otherLetters + listOf(letter)).shuffled(),
                correctLetter = letter,
                rows = 2
            )
        } else if (currentLevel <= 7) {
            val rc = colors.random()
            val letter = allKeyboardLetters.find {
                it.letter == leLetter && it.color == rc
            }!!
            val otherLetters = allKeyboardLetters.filter {
                it != letter
            }.shuffled().take(8)
            _gameState.value = GameState(
                displayedLetters = (otherLetters + listOf(letter)).shuffled(),
                correctLetter = letter,
                rows = 3
            )
        } else if (currentLevel <= 9) {
            val rc = colors.random()
            val letter = allKeyboardLetters.find {
                it.letter == leLetter && it.color == rc
            }!!
            _gameState.value = GameState(
                displayedLetters = allKeyboardLetters.shuffled(),
                correctLetter = letter,
                rows = 12
            )
        }else {
            val letter = KeyboardLetter(leLetter, Color.Magenta)
            _gameState.value = GameState(
                displayedLetters = allKeyboardLetters.shuffled(),
                correctLetter = letter,
                rows = 12
            )
        }
    }
}


fun InputStream.lines(): List<String> =
    BufferedReader(InputStreamReader(this)).lines().collect(Collectors.toList())


fun decrypt(enc: String, key: String) : String {
    val keySpec = SecretKeySpec(getHash(key), "AES")
    val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
    cipher.init(Cipher.DECRYPT_MODE, keySpec)

    val encryptedBytes = Base64.getDecoder().decode(enc)
    val decryptedBytes = cipher.doFinal(encryptedBytes)

    return String(decryptedBytes)
}

fun getHash(input: String): ByteArray {
    val md = MessageDigest.getInstance("SHA-256")
    return md.digest(input.toByteArray())
}

@Composable
fun UnfairKeyboard(gameState: GameState, success: () -> Unit) {
    Surface(
        shape = CircleShape,
        border = BorderStroke(4.dp, MaterialTheme.colorScheme.primary),
        modifier = Modifier
            .requiredWidth(200.dp)
            .requiredHeight(200.dp)
            .graphicsLayer {
                clip = true
            }
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterVertically),
            modifier = Modifier
                .padding(4.dp)
                .verticalScroll(rememberScrollState())
                .horizontalScroll(rememberScrollState())
        ) {
            repeat(gameState.rows) { y ->
                Row(
                    horizontalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    repeat(gameState.displayedLetters.size / gameState.rows) { x ->
                        val letter = gameState.displayedLetters.getOrNull(y * gameState.rows + x)
                        if (letter != null) {
                            LetterButton(letter) {
                                if (letter == gameState.correctLetter) {
                                    success()
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LetterButton(letter: KeyboardLetter, onClick: () -> Unit) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(4.dp, letter.color),
        modifier = Modifier
            .requiredWidth(48.dp)
            .requiredHeight(48.dp),
        onClick = { onClick() }
    ) {
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(letter.letter, fontWeight = FontWeight.Bold)
        }
    }
}


@Composable
fun ExampleLetterButton(letter: KeyboardLetter) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        border = BorderStroke(3.dp, letter.color),
        modifier = Modifier
            .requiredWidth(36.dp)
            .requiredHeight(36.dp)
    ) {
        Row(
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(letter.letter, fontWeight = FontWeight.Bold)
        }
    }
}
