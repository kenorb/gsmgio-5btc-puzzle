#!/usr/bin/env python3
"""
Test decryption of Cosmic Duality blob
Using the seven-token XOR method from Issue #56
"""

import base64
import hashlib
from Crypto.Cipher import AES

# Cosmic Duality blob (extracted from image)
COSMIC_BLOB = """U2FsdGVkX18/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFe
dGJh4SJIP66qRtXvo7PtpvsIjw08prLiC/sNHthxiGMugIrKo0224r0isFJZgARi
c7PaJPne4nab8XCFuV3NbfxGX2BUjNkef5hg7nsoadZx08dNyU2b6eiciWiUvu7D
SATSF07IFBiAMz7dDqIETKuG1TAP4EmMQUZrQNtfbJsURATW6V5VSbtZB5RFk00+
IymhstzrQHsU0Bugjv2nndm0EhCxGi/1qK2rLNdOOLutYGnA6RDDbFJUattggELh
2Sz+SBpCdbSGjx0ap2719FOy1o2r0HU6UxFdcsbfZ1utTqVEyNs91emQxtpgt+8
BPZisiI74Jv4EmrpRDC3ufnkmlwR8NfqVPIKhUiGDu5Qf1YjczTGDrA9vLQZu3bk
k+/ZurtRYnqgsj49UhwEF9GFuFl7uQYm0UunatW43C3Z1tyFRGAzAHQUF56jRCd+
vZGyoTlOsThjXDDCSAwoX2M+yl+oaEQoVVDuWKIqRhfDNuBmEfi+HpXuJLPBS1Pb
UjrgoG/Uv7o8IeyST4HBv8+5KLx7IKQ5t1kPZ2YUME+8XJx0caFYs+JS2Jdm0oj
Jm3JJEcYXdKEzOQvRzi4k+6dN1JO5TRZNTJvn0fPG5cM80aQb/ckUHsLsw9a4Nzh
HsrzBQRTIhog9sTm+k+LkXzIJjiFfSzRgf250pbvifGoQaIFl1CTQPT2w29DLP900
6bSiliyywwnxXOor03Hn+7MJL27YxeaGQn0sFGgP5X0X4jm3vEBkWvtF4PZ10bXWZ"""

# SalPhaselon blob (from earlier)
SALPHASELON_BLOB = """U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"""

def sha256(text: str) -> bytes:
    return hashlib.sha256(text.encode()).digest()

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(b1, b2))

def parse_salted(blob_b64: str) -> tuple:
    """Parse OpenSSL Salted__ format"""
    blob = base64.b64decode(blob_b64.replace('\n', ''))
    if blob[:8] == b'Salted__':
        salt = blob[8:16]
        ciphertext = blob[16:]
        return salt, ciphertext
    return None, blob

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16, md: str = 'md5') -> tuple:
    """OpenSSL's EVP_BytesToKey"""
    if md == 'md5':
        hash_func = hashlib.md5
    elif md == 'sha256':
        hash_func = hashlib.sha256
    else:
        hash_func = hashlib.md5

    d_i = b''
    d = b''
    while len(d) < key_len + iv_len:
        d_i = hash_func(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]

def try_decrypt(salt: bytes, ciphertext: bytes, password: bytes, md: str = 'md5') -> bytes:
    """Try AES-256-CBC decryption"""
    key, iv = evp_bytes_to_key(password, salt, md=md)
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        # Check PKCS7 padding
        padding = plaintext[-1]
        if padding <= 16 and all(p == padding for p in plaintext[-padding:]):
            return plaintext[:-padding]
        return plaintext
    except:
        return b''

def is_readable(data: bytes) -> tuple:
    if len(data) == 0:
        return False, 0.0
    printable = sum(1 for b in data if 32 <= b <= 126 or b in [9, 10, 13])
    return printable / len(data) > 0.7, printable / len(data)

# Seven tokens from Issue #56
SEVEN_TOKENS = [
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlist",  # repeated
    "yourlastcommand",
    "secondanswer"
]

def compute_seven_token_key() -> bytes:
    """Compute XOR of SHA256 hashes of seven tokens"""
    result = sha256(SEVEN_TOKENS[0])
    for token in SEVEN_TOKENS[1:]:
        result = xor_bytes(result, sha256(token))
    return result

def main():
    print("=" * 70)
    print("GSMG.IO Puzzle - Seven Token XOR Method Testing")
    print("=" * 70)

    # Compute seven-token XOR key
    seven_key = compute_seven_token_key()
    print(f"\nSeven-token XOR key (hex): {seven_key.hex()}")

    # Test both blobs
    blobs = [
        ("SalPhaselon", SALPHASELON_BLOB),
        ("Cosmic Duality", COSMIC_BLOB),
    ]

    for name, blob in blobs:
        print(f"\n--- Testing {name} blob ---")
        try:
            salt, ciphertext = parse_salted(blob)
            if salt:
                print(f"Salt: {salt.hex()}")
                print(f"Ciphertext length: {len(ciphertext)} bytes")
            else:
                print("No Salted__ header found")
                continue

            # Test with seven-token key as password
            for md in ['md5', 'sha256']:
                result = try_decrypt(salt, ciphertext, seven_key, md)
                readable, ratio = is_readable(result)
                print(f"\nUsing seven-token key as password (digest: {md})")
                print(f"Readable: {readable} (ratio: {ratio:.2f})")
                if readable:
                    print(f"Output: {result[:200]}")

            # Test with seven-token key directly as AES key
            print("\nUsing seven-token key directly as AES key...")
            # Try with salt as IV
            try:
                iv = salt + salt  # Pad to 16 bytes
                cipher = AES.new(seven_key, AES.MODE_CBC, iv)
                plaintext = cipher.decrypt(ciphertext)
                readable, ratio = is_readable(plaintext)
                print(f"With salt-based IV - Readable: {readable} (ratio: {ratio:.2f})")
                if readable:
                    print(f"Output: {plaintext[:200]}")
            except Exception as e:
                print(f"Error: {e}")

            # Try other password variations
            passwords_to_try = [
                b"matrixsumlist",
                b"enter",
                b"lastwordsbeforearchichoice",
                b"thispassword",
                sha256("matrixsumlist"),
                sha256("theseedisplanted"),
                sha256("HASHTHETEXT"),
                b"THEMATRIXHASYOU",
                b"causality",
            ]

            print("\nTrying various passwords...")
            for pwd in passwords_to_try:
                for md in ['md5', 'sha256']:
                    result = try_decrypt(salt, ciphertext, pwd, md)
                    readable, ratio = is_readable(result)
                    if readable:
                        pwd_str = pwd.hex() if isinstance(pwd, bytes) and len(pwd) == 32 else pwd
                        print(f"\n*** FOUND READABLE OUTPUT ***")
                        print(f"Password: {pwd_str}")
                        print(f"Digest: {md}")
                        print(f"Output: {result[:200]}")

        except Exception as e:
            print(f"Error parsing blob: {e}")

    print("\n" + "=" * 70)
    print("Testing complete")

if __name__ == "__main__":
    main()
