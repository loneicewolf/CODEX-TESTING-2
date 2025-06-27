# CODEX-TESTING-2
# NOT MY CODE!
# AI `MADE` (Yep. MADE. I have done NO work in this repo)
# ALL credit goes to OpenAI/`CODEX`

## Cryptography Methods

This repository includes a collection of simple cryptographic tools organised by
method and difficulty.  Each folder under `cryptography_methods/` contains three
levels of scripts:

1. **Level 1 – Basic**: naive classical techniques.
2. **Level 2 – Intermediate**: classical polyalphabetic or simple LSB methods.
3. **Level 3 – Advanced**: uses modern hashing and AES encryption combined with
   other methods.

Scripts come in two flavours:

* **Type A** – perform encryption/decryption or data hiding.
* **Type B** – attempt to analyse or break the corresponding Type A method.

### Structure

```
cryptography_methods/
    Concealment/   # steganography examples
    Transposition/ # transposition ciphers
    Substitution/  # substitution ciphers
```

Within each method folder you will find six scripts:
`level1_A.py`, `level1_B.py`, `level2_A.py`, `level2_B.py`, `level3_A.py`,
`level3_B.py`.

### Requirements

Some scripts rely on external packages such as **Pillow** or **PyCryptodome**.
Install dependencies with:

```
pip install Pillow pycryptodome
```

### Usage

Each script includes usage examples in its module docstring.  In general, run a
script with `--help` to see its options.  Example:

```
python3 cryptography_methods/Substitution/level1_A.py --help
```
