#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Comprehensive Password Testing
Based on clue analysis: "sha b e f our first hint is your last command"
"""

import subprocess
import hashlib
import itertools
from typing import Optional, Tuple

BLOB_FILE = "salphaselon_blob.txt"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def xor_hashes(hashes: list) -> str:
    """XOR multiple hex hashes together"""
    result = bytes.fromhex(hashes[0])
    for h in hashes[1:]:
        b = bytes.fromhex(h)
        result = bytes(a ^ b for a, b in zip(result, b))
    return result.hex()

def is_readable(data: bytes) -> Tuple[bool, float]:
    """Check if output is readable text"""
    if len(data) == 0:
        return False, 0.0
    printable = sum(1 for b in data if 32 <= b <= 126 or b in [9, 10, 13])
    ratio = printable / len(data)
    return ratio > 0.7, ratio

def test_password(password: str, digest: str = "") -> Optional[Tuple[str, bytes]]:
    """Test a single password"""
    cmd = ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-in", BLOB_FILE, "-pass", f"pass:{password}"]
    if digest:
        cmd.extend(["-md", digest])

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        if result.returncode == 0 and len(result.stdout) > 0:
            readable, ratio = is_readable(result.stdout)
            if readable:
                return digest, result.stdout
    except:
        pass
    return None

def test_all_digests(password: str) -> Optional[Tuple[str, str, bytes]]:
    """Test password with all digest modes"""
    for digest in ["", "md5", "sha256", "sha1", "sha512"]:
        result = test_password(password, digest)
        if result:
            return password, result[0], result[1]
    return None

# =============================================================================
# FIRST HINTS - possible interpretations
# =============================================================================
FIRST_HINTS = [
    # Phase 1 result
    "theseedisplanted",
    "gsmg.io/theseedisplanted",
    "theseedisplanted.png",

    # First decode in SalPhaselon
    "matrixsumlist",
    "matrix sum list",
    "matrixsum",

    # First phase password
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",

    # First clue reference
    "puzzle",
    "gsmg",
    "gsmgio",
    "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",

    # First password
    "causality",
]

# =============================================================================
# LAST COMMAND - possible interpretations
# =============================================================================
LAST_COMMANDS = [
    "enter",
    "ENTER",
    "Enter",
    "submit",
    "go",
    "run",
    "execute",
    "decrypt",
    "open",
]

# =============================================================================
# Key decoded elements from puzzle
# =============================================================================
DECODED_ELEMENTS = [
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "yourlastcommand",
    "secondanswer",
    "HASHTHETEXT",
    "hashthetext",
    "shabefanstoo",
]

# =============================================================================
# Matrix sum values
# =============================================================================
MATRIX_SUMS = [
    "100110001001",  # Binary mentioned in Issue #6
    "422",           # Decimal sum
    "57757457637125", # Row sums concatenated
    "5775745763712500", # With trailing
    "1a6",           # Hex of 422
    "0x1a6",
]

# =============================================================================
# Generate all passwords to test
# =============================================================================
def generate_passwords():
    passwords = []

    # 1. First hint IS your last command - literal interpretation
    # SHA256(first_hint) as password
    for hint in FIRST_HINTS:
        passwords.append(sha256(hint))
        passwords.append(md5(hint))
        passwords.append(hint)
        passwords.append(hint.lower())
        passwords.append(hint.upper())

    # 2. First hint + last command combinations
    for hint in FIRST_HINTS:
        for cmd in LAST_COMMANDS:
            combined = hint + cmd
            passwords.append(sha256(combined))
            passwords.append(combined)
            combined2 = cmd + hint
            passwords.append(sha256(combined2))
            passwords.append(combined2)

    # 3. All decoded elements as passwords
    for elem in DECODED_ELEMENTS:
        passwords.append(elem)
        passwords.append(sha256(elem))
        passwords.append(elem.lower())
        passwords.append(elem.upper())

    # 4. Matrix sums
    for s in MATRIX_SUMS:
        passwords.append(s)
        passwords.append(sha256(s))

    # 5. Combinations of decoded elements
    for combo in itertools.combinations(DECODED_ELEMENTS[:5], 2):
        combined = ''.join(combo)
        passwords.append(combined)
        passwords.append(sha256(combined))

    for combo in itertools.combinations(DECODED_ELEMENTS[:5], 3):
        combined = ''.join(combo)
        passwords.append(combined)
        passwords.append(sha256(combined))

    # 6. The seven-token password (from Issue #56)
    seven_tokens = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword", "matrixsumlist", "yourlastcommand", "secondanswer"]
    passwords.append(''.join(seven_tokens))
    passwords.append(sha256(''.join(seven_tokens)))

    # XOR of seven token hashes
    hashes = [sha256(t) for t in seven_tokens]
    xor_result = xor_hashes(hashes)
    passwords.append(xor_result)

    # 7. "fourfirsthintisyourlastcommand" parsed as password clues
    # "four" might mean 4th element or phase 4
    passwords.append("fourfirsthintisyourlastcommand")
    passwords.append(sha256("fourfirsthintisyourlastcommand"))

    # 8. "shabefanstoo" = "SHA256 fans too" or "SHA256 answer too"
    passwords.append("shabefanstoo")
    passwords.append(sha256("shabefanstoo"))
    passwords.append("sha256answertoo")
    passwords.append("sha256fanstoo")

    # 9. Architect's last words
    architect_quotes = [
        "sheisgoingtodieandthereisnothingthatyoucandotostopit",
        "sheisgoingtodieandthereisnothingcanyoucandostopit",
        "theproblemischoice",
        "hopeitisthequintessentialhumandelusion",
        "denialismostpredictableofallhumanresponses",
        "wewont",
        "asadequatelyputtheproblemischoice",
    ]
    for quote in architect_quotes:
        passwords.append(quote)
        passwords.append(sha256(quote))

    # 10. "lastwordsbeforearchichoice" interpretations
    # The literal last words before Neo makes his choice
    for quote in architect_quotes:
        passwords.append(f"lastwordsbeforearchichoice{quote}")
        passwords.append(sha256(f"lastwordsbeforearchichoice{quote}"))

    # 11. Half and better half
    passwords.append("halfandbetterhalf")
    passwords.append(sha256("halfandbetterhalf"))
    passwords.append("halfbetterhalf")
    passwords.append("theprivatekeysbelongtohalfandbetterhalf")

    # 12. From Issue #55 - the claimed key
    passwords.append("6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23")

    # 13. From Issue #65 - "SUMREMAINDERUNBALANCEDEQUATION"
    passwords.append("SUMREMAINDERUNBALANCEDEQUATION")
    passwords.append("sumremainderunbalancedequation")
    passwords.append(sha256("SUMREMAINDERUNBALANCEDEQUATION"))
    passwords.append("yourlifeisthesumofremainderunbalancedequation")

    # 14. Specific interpretations of "archi"
    archi_meanings = [
        "architect",
        "Architect",
        "archimedes",
        "Archimedes",
        "architecture",
        "arche",  # Greek for "beginning"
    ]
    for archi in archi_meanings:
        passwords.append(f"lastwordsbefore{archi}choice")
        passwords.append(sha256(f"lastwordsbefore{archi}choice"))

    # 15. Known phase passwords
    known_passwords = [
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",  # causality hash
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",  # phase 3.1
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",  # phase 3.2
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",  # puzzle hash
    ]
    passwords.extend(known_passwords)

    # 16. Try "thispassword" literally
    passwords.append("thispassword")
    passwords.append(sha256("thispassword"))
    passwords.append("this password")
    passwords.append("ThisPassword")

    # 17. Try combinations involving "secondanswer"
    passwords.append("secondanswer")
    passwords.append(sha256("secondanswer"))
    passwords.append("matrixsumlistsecondanswer")

    # 18. FEN chess notation from phase 3
    fen = "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1"
    passwords.append(fen)
    passwords.append(sha256(fen))
    passwords.append(fen.replace(" ", ""))
    passwords.append(sha256(fen.replace(" ", "")))

    # 19. Bitcoin genesis block hex
    genesis_hex = "0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854"
    passwords.append(genesis_hex)
    passwords.append(sha256(genesis_hex))

    # 20. HASHTHETEXT variations
    passwords.append("HASHTHETEXT")
    passwords.append(sha256("HASHTHETEXT"))
    passwords.append("hashthetext")
    passwords.append(sha256("hashthetext"))
    # Hash of a specific text
    passwords.append(sha256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"))

    # Remove duplicates
    return list(dict.fromkeys(passwords))

def main():
    print("=" * 70)
    print("GSMG.IO Puzzle - Comprehensive Password Testing")
    print("Based on clue: 'sha b e f our first hint is your last command'")
    print("=" * 70)

    passwords = generate_passwords()
    print(f"\nGenerated {len(passwords)} unique passwords to test")

    successes = []
    for i, password in enumerate(passwords):
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(passwords)}")

        result = test_all_digests(password)
        if result:
            pwd, digest, output = result
            print(f"\n{'*'*60}")
            print(f"*** FOUND READABLE OUTPUT ***")
            print(f"Password: {pwd}")
            print(f"Digest: {digest}")
            print(f"Output preview: {output[:200]}")
            print(f"{'*'*60}")
            successes.append(result)

    print("\n" + "=" * 70)
    print(f"Testing complete. {len(successes)} readable outputs found.")

    if successes:
        with open("comprehensive_results.txt", "w") as f:
            for pwd, digest, output in successes:
                f.write(f"Password: {pwd}\n")
                f.write(f"Digest: {digest}\n")
                f.write(f"Output:\n{output.decode('utf-8', errors='replace')}\n")
                f.write("-" * 40 + "\n")
        print("Results saved to comprehensive_results.txt")
    else:
        print("\nNo readable outputs found.")
        print("\nPossible reasons:")
        print("1. The password requires a different derivation method")
        print("2. The output is binary/encoded, not plaintext")
        print("3. Additional transformation needed on the password")
        print("4. Need to try PBKDF2 or other KDFs")

if __name__ == "__main__":
    main()
