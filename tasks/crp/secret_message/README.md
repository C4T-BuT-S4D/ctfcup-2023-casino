# rev | bad cipher

## Information

Мы нашли это секретное послание в куче мусора.

We found this secret message in a garbage pile.

## Public

Provide python file: [public/message.py](public/message.py).

## TLDR

Rsa, given `p + q mod(r)`, where `r` has less bits then `p` and `q`.

## Writeup (ru)

Решим систему уравнений `{p + q = secret (mod r); p * q = n (mod r)}` и получим `p (mod r)`, затем переберем `k`, где `p = p (mod r) + k * r`, получим `p` и расшифруем шифротекст получив `d`.

## Writeup (en)

Solve `{p + q = secret (mod r); p * q = n (mod r)}` and obtain `p (mod r)`, then bruteforce `k`, where `p = p (mod r) + k * r`, obtain `p` and decrypt the ciphertext having obtained `d`.

[Exploit](solve/solve.py)

## Flag

ctfcup{d6cdb20428eca320bb0db5ca5dd46323}
