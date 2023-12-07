from random import choices
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from base64 import b64encode

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-"
flag = "ctfcup{Gu4axf_Sbe-Cynl1at}"

for i in range(len(flag)):
    l, r = "".join(choices(chars, k=i)), "".join(choices(chars, k=len(flag)-i-1))

    x = l + flag[i] + r
    assert x[i] == flag[i]

    key = SHA256.new(flag[:i].encode()).digest()
    print(b64encode(AES.new(key, AES.MODE_ECB).encrypt(pad(x.encode(), 16))).decode())

