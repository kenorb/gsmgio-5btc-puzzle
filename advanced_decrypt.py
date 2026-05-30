#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Advanced Decryption Approaches
Try different key derivation methods and direct key/IV
"""

import base64
import hashlib
import subprocess
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os

# The SalPhaselon AES blob
BLOB_BASE64 = """U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"""

def parse_salted_blob(blob_b64: str) -> tuple:
    """Parse OpenSSL Salted__ format: Salted__ + 8-byte salt + ciphertext"""
    blob = base64.b64decode(blob_b64.replace('\n', ''))
    if blob[:8] != b'Salted__':
        raise ValueError("Not a Salted__ format")
    salt = blob[8:16]
    ciphertext = blob[16:]
    return salt, ciphertext

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16, md: str = 'md5') -> tuple:
    """
    OpenSSL's EVP_BytesToKey key derivation function
    Returns (key, iv)
    """
    d_i = b''
    d = b''

    if md == 'md5':
        hash_func = hashlib.md5
    elif md == 'sha256':
        hash_func = hashlib.sha256
    elif md == 'sha1':
        hash_func = hashlib.sha1
    elif md == 'sha512':
        hash_func = hashlib.sha512
    else:
        hash_func = hashlib.md5

    while len(d) < key_len + iv_len:
        d_i = hash_func(d_i + password + salt).digest()
        d += d_i

    return d[:key_len], d[key_len:key_len + iv_len]

def try_decrypt_with_evp(password: str, salt: bytes, ciphertext: bytes, md: str = 'md5') -> bytes:
    """Try decryption using EVP_BytesToKey derived key"""
    key, iv = evp_bytes_to_key(password.encode(), salt, md=md)
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        # Remove PKCS7 padding
        padding = plaintext[-1]
        if padding <= 16 and all(p == padding for p in plaintext[-padding:]):
            plaintext = plaintext[:-padding]
        return plaintext
    except Exception as e:
        return b''

def try_decrypt_with_pbkdf2(password: str, salt: bytes, ciphertext: bytes, iterations: int = 10000) -> bytes:
    """Try decryption using PBKDF2 key derivation"""
    try:
        key = PBKDF2(password, salt, dkLen=32, count=iterations)
        # Try different IVs
        ivs = [
            salt + salt,  # Salt repeated
            b'\x00' * 16,  # Zero IV
            hashlib.md5(salt).digest(),  # MD5 of salt
        ]
        for iv in ivs:
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = cipher.decrypt(ciphertext)
                padding = plaintext[-1]
                if padding <= 16 and all(p == padding for p in plaintext[-padding:]):
                    return plaintext[:-padding]
            except:
                pass
    except:
        pass
    return b''

def try_direct_key_iv(key_hex: str, iv_hex: str, ciphertext: bytes) -> bytes:
    """Try direct key/IV decryption"""
    try:
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        padding = plaintext[-1]
        if padding <= 16 and all(p == padding for p in plaintext[-padding:]):
            return plaintext[:-padding]
        return plaintext
    except Exception as e:
        return b''

def is_readable(data: bytes) -> tuple:
    """Check if data is readable text"""
    if len(data) == 0:
        return False, 0.0
    printable = sum(1 for b in data if 32 <= b <= 126 or b in [9, 10, 13])
    ratio = printable / len(data)
    return ratio > 0.7, ratio

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def main():
    print("=" * 70)
    print("GSMG.IO Puzzle - Advanced Decryption")
    print("=" * 70)

    # Parse the blob
    salt, ciphertext = parse_salted_blob(BLOB_BASE64)
    print(f"Salt (hex): {salt.hex()}")
    print(f"Ciphertext length: {len(ciphertext)} bytes")

    # Passwords to try
    passwords = [
        # Decoded elements
        "matrixsumlist",
        "enter",
        "lastwordsbeforearchichoice",
        "thispassword",
        "yourlastcommand",
        "secondanswer",

        # First hints
        "theseedisplanted",
        "HASHTHETEXT",
        "hashthetext",
        "causality",

        # SHA256 hashes
        sha256("matrixsumlist"),
        sha256("enter"),
        sha256("lastwordsbeforearchichoice"),
        sha256("thispassword"),
        sha256("theseedisplanted"),
        sha256("HASHTHETEXT"),
        sha256("causality"),

        # Known phase passwords
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",

        # Combinations
        "matrixsumlistenter",
        "matrixsumlistenterlastwordsbeforearchichoice",
        sha256("matrixsumlistenter"),

        # Matrix quotes
        "sheisgoingtodieandthereisnothingthatyoucandotostopit",
        "theproblemischoice",
        "THEMATRIXHASYOU",

        # Special
        "fourfirsthintisyourlastcommand",
        sha256("fourfirsthintisyourlastcommand"),
    ]

    print("\n--- Testing EVP_BytesToKey with different digests ---")
    for password in passwords:
        for md in ['md5', 'sha256', 'sha1']:
            result = try_decrypt_with_evp(password, salt, ciphertext, md)
            readable, ratio = is_readable(result)
            if readable:
                print(f"\n*** FOUND READABLE OUTPUT ***")
                print(f"Password: {password}")
                print(f"Digest: {md}")
                print(f"Output: {result[:200]}")

    print("\n--- Testing PBKDF2 with different iterations ---")
    for password in passwords[:10]:  # Test fewer due to time
        for iterations in [1, 10, 100, 1000, 10000]:
            result = try_decrypt_with_pbkdf2(password, salt, ciphertext, iterations)
            readable, ratio = is_readable(result)
            if readable:
                print(f"\n*** FOUND READABLE OUTPUT (PBKDF2) ***")
                print(f"Password: {password}")
                print(f"Iterations: {iterations}")
                print(f"Output: {result[:200]}")

    print("\n--- Testing direct key/IV from Issue #55 ---")
    key_hex = "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23"
    iv_hex = "c6ff2e39d98843bc3c26b8a33a15b5c9"
    result = try_direct_key_iv(key_hex, iv_hex, ciphertext)
    readable, ratio = is_readable(result)
    print(f"Key: {key_hex}")
    print(f"IV: {iv_hex}")
    print(f"Readable: {readable} (ratio: {ratio:.2f})")
    print(f"Output (hex): {result.hex()[:100]}...")

    # Try generating key/IV from password hashes
    print("\n--- Testing key/IV derived from password hashes ---")
    for password in passwords[:20]:
        # Use SHA256 hash as key
        key = hashlib.sha256(password.encode()).digest()
        # Try different IVs
        ivs = [
            hashlib.md5(password.encode()).digest(),
            bytes.fromhex(salt.hex() + salt.hex())[:16],
            key[:16],  # First 16 bytes of key
            b'\x00' * 16,
        ]
        for iv in ivs:
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = cipher.decrypt(ciphertext)
                # Check for valid PKCS7 padding
                padding = plaintext[-1]
                if padding <= 16 and all(p == padding for p in plaintext[-padding:]):
                    plaintext = plaintext[:-padding]
                    readable, ratio = is_readable(plaintext)
                    if readable:
                        print(f"\n*** FOUND READABLE OUTPUT ***")
                        print(f"Key from: SHA256({password})")
                        print(f"IV: {iv.hex()}")
                        print(f"Output: {plaintext[:200]}")
            except:
                pass

    print("\n" + "=" * 70)
    print("Testing complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
