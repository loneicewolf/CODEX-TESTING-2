#!/usr/bin/env python3
"""Level 1 Concealment (Type B): analyze file for appended data.

This script checks for the predefined marker used in level1_A.py and extracts
any data that follows it.

Usage:
    python3 level1_B.py <suspect_file>
"""
import sys

MARKER = b"SECRET_START"


def analyze(file_path: str) -> None:
    with open(file_path, 'rb') as f:
        data = f.read()
    idx = data.find(MARKER)
    if idx == -1:
        print('No hidden data found.')
        return
    secret = data[idx + len(MARKER):]
    print(f'Hidden data detected! ({len(secret)} bytes)')
    sys.stdout.buffer.write(secret)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 level1_B.py <suspect_file>')
        sys.exit(1)
    analyze(sys.argv[1])
