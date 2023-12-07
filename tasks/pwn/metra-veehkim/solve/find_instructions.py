#!/usr/bin/env python3
from pwn import *
from subprocess import check_output
from itertools import product


q = set()
for i in product(set(b' Metra_Veehkim'),repeat=3):
    s = bytes(list(i)+[0x61,0x61,0x61,0x61,0x61]).hex()
    a = check_output(["rasm2","-d",f"{s}"])
    for x in a.decode().split('\n'):
        q.add(x)

for i in sorted(list(q)):
    print(i, flush=True)
