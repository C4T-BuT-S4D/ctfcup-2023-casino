# rev | C4Tpixx
## Information

Мы тут не всё успели доделать... (Сами понимаете, айти бюджеты на Metra Veehkim невелики.) Но зацените то, что есть! Надеемся, у вас получится разглядеть что-то любопытное.

## Deploy

## Public
Give [zip archive](public/rev-catpixx.zip).

## TL;DR
The app's code was minified, so we'll have to look for clues. One such clue is `android.widget.Toast` shown when we're wrong. We find one suspicious usage in `XXX()`. The method names of xrefs to `XXX()` spell out the flag. This can be seen in logcat, because if we enter the correct secret string, the app crashes with UnsupportedOperationException.

## Flag
`ctfcup{suchnicec4tpixxwo4h}`
