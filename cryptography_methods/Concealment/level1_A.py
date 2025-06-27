#!/usr/bin/env python3
"""Level 1 Concealment (Type A): append secret data to a cover file.

Usage:
    python3 level1_A.py hide <cover_file> <secret_file> <output_file>
    python3 level1_A.py extract <stego_file> <output_secret>
"""
import argparse

MARKER = b"SECRET_START"


def hide(cover_file: str, secret_file: str, output_file: str) -> None:
    with open(cover_file, 'rb') as cf, open(secret_file, 'rb') as sf, open(output_file, 'wb') as out:
        out.write(cf.read())
        out.write(MARKER)
        out.write(sf.read())


def extract(stego_file: str, output_secret: str) -> None:
    with open(stego_file, 'rb') as f:
        data = f.read()
    index = data.find(MARKER)
    if index == -1:
        raise ValueError('Marker not found: no hidden data.')
    secret = data[index + len(MARKER):]
    with open(output_secret, 'wb') as out:
        out.write(secret)


def main():
    p = argparse.ArgumentParser(description='Basic concealment by appending data.')
    sub = p.add_subparsers(dest='cmd', required=True)

    h = sub.add_parser('hide', help='Hide secret file inside cover file.')
    h.add_argument('cover_file')
    h.add_argument('secret_file')
    h.add_argument('output_file')

    e = sub.add_parser('extract', help='Extract hidden data from stego file.')
    e.add_argument('stego_file')
    e.add_argument('output_secret')

    args = p.parse_args()
    if args.cmd == 'hide':
        hide(args.cover_file, args.secret_file, args.output_file)
    else:
        extract(args.stego_file, args.output_secret)


if __name__ == '__main__':
    main()
