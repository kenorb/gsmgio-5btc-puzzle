#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Massive Password Testing
Try 1000+ more password combinations
"""

import subprocess
import hashlib
import itertools
import string
from typing import Optional

BLOB_FILE = "salphaselon_blob.txt"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def test_password(password: str) -> Optional[str]:
    """Test password with openssl"""
    for digest in ["", "-md md5", "-md sha256", "-md sha1"]:
        cmd = f'openssl enc -aes-256-cbc -d -a {digest} -in {BLOB_FILE} -pass "pass:{password}" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0 and len(result.stdout) > 0:
            output = result.stdout
            printable = sum(1 for b in output if 32 <= b <= 126 or b in [9, 10, 13])
            if printable / len(output) > 0.7:
                return output.decode('utf-8', errors='replace')
    return None

# Generate massive password list
passwords = set()

# ============================================
# MATRIX QUOTES - Every significant line
# ============================================
matrix_quotes = [
    # Architect's complete speech fragments
    "she is going to die",
    "there is nothing that you can do to stop it",
    "nothing you can do",
    "an emotion that is already blinding you",
    "simple and obvious truth",
    "simple obvious truth",
    "hope it is the quintessential human delusion",
    "quintessential human delusion",
    "your greatest strength",
    "your greatest weakness",
    "source of your greatest strength and greatest weakness",
    "denial is the most predictable",
    "most predictable of all human responses",
    "function of the one",
    "return to the source",
    "salvation of zion",
    "end of your species",
    "the problem is choice",
    "problem is choice",
    "as you adequately put",
    "we already know",
    "we already know what you are going to do",

    # Neo's lines
    "i dont believe it",
    "i choose to",
    "because i choose to",
    "bullshit",

    # Oracle
    "everything that has a beginning has an end",
    "you have already made the choice",
    "now you have to understand it",

    # Morpheus
    "free your mind",
    "there is no spoon",
    "wake up neo",
    "the matrix has you",
    "follow the white rabbit",
    "welcome to the real world",
    "knowing the path",
    "walking the path",

    # Smith
    "mr anderson",
    "purpose",
    "inevitability",
    "why mr anderson",

    # Merovingian
    "causality",
    "cause and effect",
    "choice is an illusion",
    "those with power",
    "those without",

    # Train man
    "down here i make the rules",

    # Keymaker
    "one door",
    "another door",
    "all doors",

    # General
    "the one",
    "the anomaly",
    "zion",
    "matrix",
    "source",
    "choice",
    "door",
    "left door",
    "right door",
    "red pill",
    "blue pill",
]

# Add all variations
for quote in matrix_quotes:
    passwords.add(quote)
    passwords.add(quote.replace(" ", ""))
    clean = ''.join(c for c in quote if c.isalnum())
    passwords.add(clean)
    passwords.add(clean.lower())
    passwords.add(clean.upper())
    # SHA256 versions
    passwords.add(sha256(quote))
    passwords.add(sha256(quote.replace(" ", "")))
    passwords.add(sha256(clean))

# ============================================
# DECODED PUZZLE ELEMENTS
# ============================================
decoded = [
    "matrixsumlist", "enter", "lastwordsbeforearchichoice",
    "thispassword", "yourlastcommand", "secondanswer",
    "theseedisplanted", "HASHTHETEXT", "hashthetext",
    "shabef", "shabefanstoo", "fourfirsthintisyourlastcommand",
]

for elem in decoded:
    passwords.add(elem)
    passwords.add(elem.lower())
    passwords.add(elem.upper())
    passwords.add(sha256(elem))
    passwords.add(md5(elem))

# Combinations of 2
for i, e1 in enumerate(decoded):
    for e2 in decoded[i+1:]:
        passwords.add(e1 + e2)
        passwords.add(e2 + e1)
        passwords.add(sha256(e1 + e2))

# ============================================
# NUMERIC VALUES
# ============================================
numbers = [
    "422", "57", "75", "74", "63", "71", "25",
    "100110001001", "110100110",
    "57757457637125", "5775745763712500",
    "1a6", "0x1a6",
    "11110", "1141",
    "23", "16", "7", "23167", "16723",
]
for n in numbers:
    passwords.add(n)
    passwords.add(sha256(n))

# ============================================
# ARCHIMEDES VARIATIONS
# ============================================
archimedes = [
    "noli turbare circulos meos",
    "noliturbarecirculosmeos",
    "do not disturb my circles",
    "donotdisturbmycircles",
    "dontdisturbmycircles",
    "stand away fellow from my diagram",
    "eureka",
    "give me a lever",
    "archimedes",
    "Archimedes",
]
for a in archimedes:
    passwords.add(a)
    passwords.add(a.replace(" ", ""))
    passwords.add(sha256(a))

# ============================================
# "LAST WORDS BEFORE ARCHI CHOICE" INTERPRETATIONS
# ============================================
# What are the actual last words before Neo's choice?
last_words_options = [
    "she is going to die and there is nothing that you can do to stop it",
    "sheisgoingtodieandthereisnothingthatyoucandotostopit",
    "an emotion blinding you from the simple obvious truth she is going to die",
    "theproblemischoice",
    "asadequatelyputtheproblemischoice",
    "wealreadyknowwhatyouaregoingto",
]
for lw in last_words_options:
    passwords.add(lw)
    passwords.add(lw.replace(" ", ""))
    passwords.add(sha256(lw))
    passwords.add(sha256(lw.replace(" ", "")))
    # With "lastwordsbeforearchichoice" prefix
    passwords.add("lastwordsbeforearchichoice" + lw.replace(" ", ""))
    passwords.add(sha256("lastwordsbeforearchichoice" + lw.replace(" ", "")))

# ============================================
# KNOWN HASHES AND KEYS
# ============================================
known_hashes = [
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
    "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
    "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",
    "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    "a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735",
    "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23",
    "4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081",
    "e7546e3076294907ed2a0ecaa9c33062f6e602b7c74c5aa5cc865df0ff345507",
    "e08d706b3e4ce964b632746cf568913cb93f1ed36476fbb0494b80ed17c5975c",
    "77094e7a1591fb81379f1582cf88db5aa6ab8e77176a4d8428a1ff5decfd102d",
    "74c1d7592daf4f89b0a7ba5e368bb59cc9e19c6a4ebb7f33cd8ccf8f3edacac0",
    "5968dc5e02cbdf8181d135f143372e7062504cc06268e094ceae25b56c5a72ae",
    "6e3f5a7baf924d8546f5f7af94a43b8424e3c810983f9795eb8451ad4243d860",
]
passwords.update(known_hashes)

# ============================================
# BITCOIN / CRYPTO
# ============================================
crypto_terms = [
    "satoshi", "nakamoto", "satoshinakamoto",
    "bitcoin", "blockchain", "genesis", "genesisblock",
    "privatekey", "publickey", "wallet",
    "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
    "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
    "halving", "halveandbetterhalf", "halfandbetterhalf",
    "fundstolive", "needfundstolive",
]
for ct in crypto_terms:
    passwords.add(ct)
    passwords.add(ct.lower())
    passwords.add(sha256(ct))

# ============================================
# PREVIOUS PHASE PASSWORDS
# ============================================
phase_passwords = [
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
    "causality",
    "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
    "THEMATRIXHASYOU",
    "causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
]
for pp in phase_passwords:
    passwords.add(pp)
    passwords.add(sha256(pp))

# ============================================
# SPECIAL COMBINATIONS
# ============================================
# "our first hint is your last command"
first_hints = ["theseedisplanted", "matrixsumlist", "puzzle", "gsmg"]
last_commands = ["enter", "submit", "go", "execute"]
for fh in first_hints:
    for lc in last_commands:
        passwords.add(sha256(fh) + lc)
        passwords.add(fh + lc)
        passwords.add(sha256(fh + lc))
        passwords.add(lc + sha256(fh))

# Row sums
passwords.add("57,75,74,57,63,71,25")
passwords.add("57 75 74 57 63 71 25")
passwords.add(sha256("57,75,74,57,63,71,25"))

# ============================================
# ISSUE #65 CLUES
# ============================================
issue65 = [
    "SUMREMAINDERUNBALANCEDEQUATION",
    "sumremainderunbalancedequation",
    "THEPUZZLEENDSWHENSTART",
    "thepuzzleendswhenstart",
    "build",
    "BUILD",
    "starttobuild",
]
for i65 in issue65:
    passwords.add(i65)
    passwords.add(sha256(i65))

# ============================================
# MISCELLANEOUS
# ============================================
misc = [
    "password", "secret", "key", "puzzle", "answer",
    "solution", "decrypt", "unlock", "open",
    "whiterabbit", "followthewhiterabbit",
    "decentraland", "-41,-17", "4117",
    "beaufort", "Beaufort", "BEAUFORT",
    "vic", "VIC", "viccpher",
    "FUBCDORA.LETHINGKYMVPS.JQZXW",
    "fubcdoralethingkymvpsjqzxw",
    "cosmicduality", "CosmicDuality", "salphaselon", "SalPhaselon",
]
passwords.update(misc)

# ============================================
# TEST ALL PASSWORDS
# ============================================
print(f"Testing {len(passwords)} unique passwords...")

count = 0
for pwd in passwords:
    count += 1
    if count % 200 == 0:
        print(f"Progress: {count}/{len(passwords)}")

    result = test_password(pwd)
    if result:
        print(f"\n{'*'*60}")
        print(f"*** FOUND READABLE OUTPUT ***")
        print(f"Password: {pwd}")
        print(f"Output: {result[:300]}")
        print(f"{'*'*60}")
        # Save result
        with open("massive_test_results.txt", "a") as f:
            f.write(f"Password: {pwd}\n")
            f.write(f"Output:\n{result}\n")
            f.write("="*40 + "\n")

print(f"\nTesting complete. Checked {len(passwords)} passwords.")
