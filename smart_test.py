#!/usr/bin/env python3
"""
GSMG.IO 5 BTC Puzzle - Smart Password Tester
Tests passwords and validates output as readable text
"""

import subprocess
import hashlib
import itertools
import string
from typing import List, Optional, Tuple

BLOB_FILE = "salphaselon_blob.txt"
RESULTS_FILE = "smart_test_results.txt"

def sha256(text: str) -> str:
    """Calculate SHA256 hash of text"""
    return hashlib.sha256(text.encode()).hexdigest()

def is_printable_text(data: bytes, threshold: float = 0.8) -> Tuple[bool, float]:
    """Check if data is mostly printable ASCII text"""
    if len(data) == 0:
        return False, 0.0
    printable_chars = sum(1 for b in data if 32 <= b <= 126 or b in [9, 10, 13])
    ratio = printable_chars / len(data)
    return ratio >= threshold, ratio

def test_password(password: str, digest: str = "") -> Optional[str]:
    """Test a password against the AES blob"""
    cmd = ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-in", BLOB_FILE, "-pass", f"pass:{password}"]
    if digest:
        cmd.extend(["-md", digest])

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        if result.returncode == 0:
            output = result.stdout
            is_text, ratio = is_printable_text(output)
            if is_text:
                return output.decode('utf-8', errors='replace')
    except:
        pass
    return None

def test_password_all_digests(password: str) -> Optional[Tuple[str, str]]:
    """Test password with all digest modes"""
    for digest in ["", "md5", "sha256", "sha1", "sha512"]:
        result = test_password(password, digest)
        if result:
            return result, digest
    return None

def generate_matrix_passwords() -> List[str]:
    """Generate Matrix-related passwords"""
    base_quotes = [
        # Architect's exact last words before Neo's choice
        "she is going to die and there is nothing that you can do to stop it",
        "she is going to die, and there is nothing that you can do to stop it",
        "an emotion that is already blinding you from the simple and obvious truth",
        "an emotion that is already blinding you",
        "the simple and obvious truth",
        "hope it is the quintessential human delusion",
        "hope is the quintessential human delusion",
        "the quintessential human delusion simultaneously the source of your greatest strength and your greatest weakness",
        "as you adequately put the problem is choice",
        "the problem is choice",
        "choice the problem is choice",
        "there are two doors",
        "the door to your right leads to the source and the salvation of zion",
        "the door to your left leads back to the matrix to her and to the end of your species",
        "we already know what you are going to do",
        "denial is the most predictable of all human responses",
        "the function of the one is now to return to the source",
        "return to the source",
        "if i were you i would hope that we dont meet again",
        "we wont",
        # Oracle quotes
        "you have already made the choice now you have to understand it",
        "everything that has a beginning has an end",
        # Merovingian quotes
        "choice is an illusion created between those with power and those without",
        "there is only one constant one universal causality cause and effect",
        # Neo quotes
        "i dont believe it",
        "because i choose to",
        # Morpheus
        "free your mind",
        "there is a difference between knowing the path and walking the path",
        "the matrix has you",
        "wake up neo",
        "welcome to the real world",
    ]

    passwords = []
    for quote in base_quotes:
        # Original with spaces
        passwords.append(quote)
        # No spaces
        passwords.append(quote.replace(" ", ""))
        # No spaces, no punctuation
        clean = ''.join(c for c in quote if c.isalnum())
        passwords.append(clean)
        passwords.append(clean.lower())
        passwords.append(clean.upper())
        # First letters of each word
        words = quote.split()
        if len(words) > 3:
            passwords.append(''.join(w[0] for w in words))

    return passwords

def generate_decoded_passwords() -> List[str]:
    """Generate passwords from decoded puzzle elements"""
    decoded = [
        "matrixsumlist",
        "enter",
        "lastwordsbeforearchichoice",
        "thispassword",
        "yourlastcommand",
        "secondanswer",
        "theseedisplanted",
        "HASHTHETEXT",
        "hashthetext",
        "shabef",
        "shabefanstoo",
    ]

    passwords = []

    # Individual elements
    for d in decoded:
        passwords.append(d)
        passwords.append(d.lower())
        passwords.append(d.upper())
        passwords.append(sha256(d))
        passwords.append(sha256(d.lower()))
        passwords.append(sha256(d.upper()))

    # Combinations of 2
    for i in range(len(decoded)):
        for j in range(len(decoded)):
            if i != j:
                combined = decoded[i] + decoded[j]
                passwords.append(combined)
                passwords.append(sha256(combined))

    # Combinations of 3
    for combo in itertools.combinations(decoded[:5], 3):
        combined = ''.join(combo)
        passwords.append(combined)
        passwords.append(sha256(combined))

    # The 7-token sequence from Issue #56
    seven_tokens = [
        "matrixsumlist", "enter", "lastwordsbeforearchichoice",
        "thispassword", "matrixsumlist", "yourlastcommand", "secondanswer"
    ]
    passwords.append(''.join(seven_tokens))
    passwords.append(sha256(''.join(seven_tokens)))

    return passwords

def generate_archimedes_passwords() -> List[str]:
    """Generate Archimedes-related passwords (alternative meaning of 'archi')"""
    quotes = [
        # Famous last words
        "do not disturb my circles",
        "dont disturb my circles",
        "noli turbare circulos meos",
        "stand away fellow from my diagram",
        "i beg of you do not disturb this",
        # Famous quotes
        "give me a lever long enough and a fulcrum on which to place it and i shall move the world",
        "eureka",
        "give me a place to stand and i will move the earth",
    ]

    passwords = []
    for quote in quotes:
        passwords.append(quote)
        passwords.append(quote.replace(" ", ""))
        clean = ''.join(c for c in quote if c.isalnum())
        passwords.append(clean)
        passwords.append(clean.lower())

    # Direct interpretations
    passwords.extend([
        "archimedes", "Archimedes", "ARCHIMEDES",
        "archi", "Archi", "ARCHI",
        "circles", "mycircles", "disturb",
        "archimedesLastWords", "archimedesLastwordsbeforeChoice",
    ])

    return passwords

def generate_first_hint_passwords() -> List[str]:
    """Generate passwords based on 'first hint is your last command' clue"""
    first_hints = [
        "theseedisplanted",
        "gsmg.io/theseedisplanted",
        "matrixsumlist",
        "causality",
        "puzzle",
        "gsmg",
    ]

    passwords = []
    for hint in first_hints:
        passwords.append(hint)
        passwords.append(sha256(hint))
        # "your last command" variations
        passwords.append(f"{hint}enter")
        passwords.append(sha256(f"{hint}enter"))

    return passwords

def generate_numeric_passwords() -> List[str]:
    """Generate passwords from numeric clues"""
    # Matrix sums: rows are 57, 75, 74, 57, 63, 71, 25, total = 422
    row_sums = [57, 75, 74, 57, 63, 71, 25]
    total = 422

    passwords = [
        str(total),
        bin(total)[2:],  # binary: 110100110
        hex(total)[2:],  # hex: 1a6
        ','.join(str(x) for x in row_sums),
        ''.join(str(x) for x in row_sums),
        str(sum(row_sums)),
        # As text
        "fourhundredtwentytwo",
        "four two two",
        "422",
        "100110001001",  # different binary?
        "2441",  # reverse?
    ]

    # From previous phases
    passwords.extend([
        "11110",  # Executive Order
        "1141",   # EBCDIC encoding
        "23",     # number of ciphers
        "16",     # number of encryptions
        "7",      # number of passwords
        "23167",
        "16723",
        "71623",
    ])

    return passwords

def generate_combination_passwords() -> List[str]:
    """Generate various combinations"""
    parts = [
        "matrixsumlist", "enter", "lastwordsbeforearchichoice",
        "thispassword", "yourlastcommand", "secondanswer",
        "theseedisplanted", "causality", "HASHTHETEXT"
    ]

    passwords = []

    # XOR of SHA256 hashes (as hex string password)
    def xor_hashes(strings: List[str]) -> str:
        result = bytes.fromhex(sha256(strings[0]))
        for s in strings[1:]:
            h = bytes.fromhex(sha256(s))
            result = bytes(a ^ b for a, b in zip(result, h))
        return result.hex()

    # Various XOR combinations
    combinations_to_try = [
        ["matrixsumlist", "enter"],
        ["matrixsumlist", "enter", "lastwordsbeforearchichoice"],
        ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"],
        ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword", "matrixsumlist"],
        ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword", "matrixsumlist", "yourlastcommand", "secondanswer"],
        ["theseedisplanted", "matrixsumlist"],
        ["HASHTHETEXT", "matrixsumlist"],
        ["causality", "matrixsumlist"],
    ]

    for combo in combinations_to_try:
        passwords.append(xor_hashes(combo))

    return passwords

def generate_special_passwords() -> List[str]:
    """Generate special/misc passwords"""
    return [
        # Previous phase passwords
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "causality",
        "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
        "THEMATRIXHASYOU",
        # Phase 3.1 7-part key
        "causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
        # Known hashes
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",  # causality
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",  # phase 3.1
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",  # phase 3.2
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",  # puzzle text hash
        # Cosmic duality key/IV from Issue #55
        "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23",
        # Simple/common
        "password", "secret", "key", "puzzle", "bitcoin", "satoshi",
        "privatekey", "publickey", "wallet",
        # Half and better half
        "halfandbetterhalf", "half and better half",
        "halfbetterhalf", "half better half",
        "fundsToLive", "fundstolive", "needfundstolive",
        # GSMG related
        "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
        "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
        "gsmgio", "GSMGIO",
        # Decentraland
        "-41,-17", "-41-17", "4117", "whiterabbitseverywhere",
        # VIC cipher related
        "FUBCDORA.LETHINGKYMVPS.JQZXW", "fubcdoralethingkymvpsjqzxw",
    ]

def main():
    print("=" * 60)
    print("GSMG.IO 5 BTC Puzzle - Smart Password Tester")
    print("=" * 60)

    all_passwords = []

    print("\nGenerating password lists...")
    all_passwords.extend(generate_matrix_passwords())
    all_passwords.extend(generate_decoded_passwords())
    all_passwords.extend(generate_archimedes_passwords())
    all_passwords.extend(generate_first_hint_passwords())
    all_passwords.extend(generate_numeric_passwords())
    all_passwords.extend(generate_combination_passwords())
    all_passwords.extend(generate_special_passwords())

    # Remove duplicates while preserving order
    seen = set()
    unique_passwords = []
    for p in all_passwords:
        if p not in seen:
            seen.add(p)
            unique_passwords.append(p)

    print(f"Testing {len(unique_passwords)} unique passwords...")

    successes = []

    for i, password in enumerate(unique_passwords):
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(unique_passwords)}")

        result = test_password_all_digests(password)
        if result:
            text, digest = result
            print(f"\n*** FOUND READABLE OUTPUT ***")
            print(f"Password: {password}")
            print(f"Digest: {digest}")
            print(f"Output: {text[:200]}...")
            successes.append((password, digest, text))

    print("\n" + "=" * 60)
    print(f"Testing complete. {len(successes)} potential matches found.")

    with open(RESULTS_FILE, 'w') as f:
        f.write("GSMG.IO Puzzle - Smart Test Results\n")
        f.write("=" * 40 + "\n\n")
        for password, digest, text in successes:
            f.write(f"Password: {password}\n")
            f.write(f"Digest: {digest}\n")
            f.write(f"Output:\n{text}\n")
            f.write("-" * 40 + "\n\n")

    if successes:
        print(f"Results saved to {RESULTS_FILE}")
    else:
        print("No readable output found with tested passwords.")

if __name__ == "__main__":
    main()
