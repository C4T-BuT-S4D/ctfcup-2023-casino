# rev | Bad Cipher

## Information

Ужасный шифр, используемый Арбалетами Сибири по неизвестной причине до сих пор.

A terrible cipher still used by Arbalest of Siberia for some unknown reason.

## Public

Provide zip archive: [public/bad-cipher.zip](public/bad-cipher.zip).

## TLDR

A simple block cipher with `SBOX[x] = x ^ 42`.

## Writeup (ru)

Нам дан простой блочный шифр и зашифрованная картинка. Однако используется один `SBOX` и для шифрования и дешифрования. На поверку оказывается, что `SBOX[x] = x ^ 42`. Таким образом один раунд шифрования просто применяет `PBOX`, ксорит данные с ключом и `42`, а само шифрование это применный 15 раз `pbox`, ксор с некоторыми элементами ключа `xor_key` и `42` 15 раз (или 1 раз). Мы можем инвертировать `PBOX` и зная первые 16 байт (один блок, png хеадер) данных получить `xor_key` и с помошью него расшифровать всю картинку.

## Writeup (en)

We are given a simple block cipher and an encrypted image. However `SBOX` is used both for encryption and decryption. Turns out `SBOX[x] = x ^ 42`. Thus an encryption round is equivalent to applying `PBOX`, xoring data with the key and `42`. The encryption itself is just `PBOX` applied 15 times, xoring with some elements of the key `xor_key` and `42` 15 times (or 1 times). We can invert `PBOX` and knowing the first 16 bytes of the message (one block, png header) and recover `xor_key` and with it decrypt the whole image.

[Exploit](solve/solve.py)

## Flag

ctfcup{b8397767f249b59941c7edb3984fb43a}
