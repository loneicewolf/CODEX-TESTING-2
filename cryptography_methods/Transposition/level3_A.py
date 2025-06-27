#!/usr/bin/env python3
"""Level 3 Transposition (Type A): AES encryption followed by columnar transposition.

Requires PyCryptodome for AES.

Usage:
    python3 level3_A.py encrypt <password> <key> <text_file>
    python3 level3_A.py decrypt <password> <key> <text_file>
"""
import argparse
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def columnar_encrypt(text: str, key: str) -> str:
    cols = len(key)
    grid = ['' for _ in range(cols)]
    for idx, ch in enumerate(text):
        grid[idx % cols] += ch
    order = sorted(range(cols), key=lambda i: key[i])
    return ''.join(grid[i] for i in order)


def columnar_decrypt(text: str, key: str) -> str:
    cols = len(key)
    rows = (len(text) + cols - 1) // cols
    order = sorted(range(cols), key=lambda i: key[i])
    lengths = [rows] * cols
    short_cols = cols * rows - len(text)
    for i in range(short_cols):
        lengths[order[-(i + 1)]] -= 1
    chunks = {}
    pos = 0
    for idx in order:
        chunks[idx] = text[pos:pos + lengths[idx]]
        pos += lengths[idx]
    result = []
    for r in range(rows):
        for c in range(cols):
            if r < len(chunks[c]):
                result.append(chunks[c][r])
    return ''.join(result)


def encrypt_file(password: str, key: str, text_file: str) -> str:
    with open(text_file, 'rb') as f:
        data = f.read()
    aes_key = derive_key(password)
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ct = cipher.iv + cipher.encrypt(pad(data, BLOCK_SIZE))
    return columnar_encrypt(ct.hex(), key)


def decrypt_file(password: str, key: str, text_file: str) -> bytes:
    with open(text_file) as f:
        cipher_text = f.read().strip()
    aes_key = derive_key(password)
    ct_hex = columnar_decrypt(cipher_text, key)
    ct = bytes.fromhex(ct_hex)
    iv = ct[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct[16:]), BLOCK_SIZE)


def main():
    p = argparse.ArgumentParser(description='AES + columnar transposition cipher')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('password')
    p.add_argument('key')
    p.add_argument('text_file')
    args = p.parse_args()
    if args.mode == 'encrypt':
        result = encrypt_file(args.password, args.key, args.text_file)
        print(result)
    else:
        data = decrypt_file(args.password, args.key, args.text_file)
        sys.stdout.buffer.write(data)


if __name__ == '__main__':
    import sys
    main()
