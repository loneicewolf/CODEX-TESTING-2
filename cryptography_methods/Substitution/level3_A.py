#!/usr/bin/env python3
"""Level 3 Substitution (Type A): AES encryption with password-derived key.

Requires PyCryptodome.

Usage:
    python3 level3_A.py encrypt <password> <text_file>
    python3 level3_A.py decrypt <password> <cipher_file>
"""
import argparse
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def encrypt_file(password: str, text_file: str) -> bytes:
    with open(text_file, 'rb') as f:
        data = f.read()
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(data, BLOCK_SIZE))


def decrypt_file(password: str, cipher_file: str) -> bytes:
    with open(cipher_file, 'rb') as f:
        data = f.read()
    key = derive_key(password)
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data[16:]), BLOCK_SIZE)


def main():
    p = argparse.ArgumentParser(description='AES encryption using SHA-256 key')
    p.add_argument('mode', choices=['encrypt', 'decrypt'])
    p.add_argument('password')
    p.add_argument('file')
    p.add_argument('output')
    args = p.parse_args()
    if args.mode == 'encrypt':
        ct = encrypt_file(args.password, args.file)
        with open(args.output, 'wb') as f:
            f.write(ct)
    else:
        pt = decrypt_file(args.password, args.file)
        with open(args.output, 'wb') as f:
            f.write(pt)


if __name__ == '__main__':
    main()
