# crp | Old Cipher

## Information

Ужасный шифр, используемый Арбалетами Сибири по неизвестной причине до сих пор.

A terrible cipher still used by Arbalest of Siberia for some unknown reason.

## Public

Provide zip archive: [public/old-cipher.zip](public/old-cipher.zip).

## TLDR

A simple block cipher with `SBOX[x] = x ^ 42`.

## Writeup (ru)

Нам дан простой блочный шифр и зашифрованная картинка. Однако используется один `SBOX` и для шифрования и дешифрования. Нетрудно заметить, что `SBOX[x] = x ^ 42`. Рассмотрим подробнее один раунд шифрования `block[i] = block[PBOX[i]] ^ key[PBOX[i]] ^ 42`. Таким образом все шифрование представляется в виде `block16[i] = block15[PBOX[i]] ^ key[PBOX[i]] ^ 42 = block15[PBOX[PBOX[i]]] ^ key[PBOX[PBOX[i]]] ^ 42 ^ key[PBOX[i]] ^ 42 = ... = block0[PBOX[... PBOX[i] ...]] ^ key[PBOX[... PBOX[i] ...]] ^ 42 ^ ... ^ key[PBOX[i]] ^ 42 = block0[PBOX[... PBOX[i] ...]] ^ xor_key[i]`, где `xor_key` - некая переменная, зависящая от ключа. Не трудно заметить что это просто применненный `16` раз `PBOX` проксоренный с `xor_key`. Зная один блок шифрования (хедер png) мы можем посчитать `block0[PBOX[... PBOX[i] ...]] ^ block16[i] = xor_key[i]` и востанновить `xor_key`. Затем зная `xor_key`, мы можем получить `block0[i] = (block16 ^ xor_key)[PBOX_INV[... PBOX_INV[i] ...]]`.


[Exploit](solve/solve.py)

## Flag

ctfcup{b8397767f249b59941c7edb3984fb43a}
