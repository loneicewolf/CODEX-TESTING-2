#!/usr/bin/env python3
"""Level 3 Transposition (Type B): dictionary attack on AES+columnar cipher.

Usage:
    python3 level3_B.py <cipher_file> <wordlist_file> <key>
The cipher_file should contain the columnar-transposed hex string produced by
level3_A.py.
"""
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

BLOCK_SIZE = 16


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


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


def try_decrypt(cipher_text: str, password: str, key: str) -> bytes:
    aes_key = derive_key(password)
    ct_hex = columnar_decrypt(cipher_text, key)
    ct = bytes.fromhex(ct_hex)
    iv = ct[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    try:
        return unpad(cipher.decrypt(ct[16:]), BLOCK_SIZE)
    except ValueError:
        return b''


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 level3_B.py <cipher_file> <wordlist_file> <key>')
        sys.exit(1)
    with open(sys.argv[1]) as cf:
        cipher_text = cf.read().strip()
    with open(sys.argv[2]) as wf:
        words = [w.strip() for w in wf]
    key = sys.argv[3]
    for word in words:
        plain = try_decrypt(cipher_text, word, key)
        if plain:
            print(f'Password found: {word}')
            sys.stdout.buffer.write(plain)
            break
