#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Final comprehensive test based on all findings
"""

import hashlib
import subprocess
import itertools

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def test_password(password, blob_file="salphaselon_blob.txt"):
    """Test password with multiple digest options"""
    for digest in ["", "-md md5", "-md sha256", "-md sha1", "-md sha512"]:
        cmd = f'openssl enc -aes-256-cbc -d -a {digest} -in {blob_file} -pass "pass:{password}" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0 and len(result.stdout) > 0:
            output = result.stdout
            printable = sum(1 for b in output if 32 <= b <= 126 or b in [9, 10, 13])
            if len(output) > 0 and printable / len(output) > 0.7:
                return output.decode('utf-8', errors='replace'), digest
    return None, None

def xor_hashes(strings):
    """XOR SHA256 hashes of multiple strings"""
    result = bytes.fromhex(sha256(strings[0]))
    for s in strings[1:]:
        h = bytes.fromhex(sha256(s))
        result = bytes(a ^ b for a, b in zip(result, h))
    return result.hex()

# ============================================
# THE EXACT DECODED ELEMENTS FROM README
# ============================================
DECODED = {
    "binary1": "matrixsumlist",  # from abba section 1
    "binary2": "enter",          # from abba section 2
    "encoded1": "lastwordsbeforearchichoice",  # a1z26 + base16 + hex
    "encoded2": "thispassword",   # a1z26 + base16 + hex
}

# ============================================
# THE SEVEN TOKENS FROM ISSUE #56
# ============================================
SEVEN_TOKENS = [
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlist",  # repeated
    "yourlastcommand",
    "secondanswer"
]

# ============================================
# THE CLUE: "sha b e f our first hint is your last command"
# sha = SHA256
# b e f = 256 (b=2, e=5, f=6)
# our first hint = one of: theseedisplanted, matrixsumlist
# is your last command = use as the final password?
# ============================================

passwords = set()

# 1. Direct decoded elements
for key, val in DECODED.items():
    passwords.add(val)
    passwords.add(sha256(val))

# 2. Combinations of decoded elements
for combo in itertools.permutations(DECODED.values(), 2):
    passwords.add(''.join(combo))
    passwords.add(sha256(''.join(combo)))

for combo in itertools.permutations(DECODED.values(), 3):
    passwords.add(''.join(combo))
    passwords.add(sha256(''.join(combo)))

for combo in itertools.permutations(DECODED.values(), 4):
    passwords.add(''.join(combo))
    passwords.add(sha256(''.join(combo)))

# 3. Seven token XOR
seven_xor = xor_hashes(SEVEN_TOKENS)
passwords.add(seven_xor)
print(f"Seven token XOR: {seven_xor}")

# 4. Different XOR combinations
for i in range(2, 8):
    for combo in itertools.combinations(SEVEN_TOKENS[:4], i):
        passwords.add(xor_hashes(list(combo)))

# 5. "First hint is your last command" interpretations
first_hints = ["theseedisplanted", "matrixsumlist", "gsmg.io/theseedisplanted"]
for fh in first_hints:
    passwords.add(sha256(fh))
    passwords.add(fh)
    # SHA256(first_hint) as password
    passwords.add(sha256(fh))
    # SHA256(SHA256(first_hint)) - double hash
    passwords.add(sha256(sha256(fh)))

# 6. "thispassword" - maybe it's literally telling us to use "thispassword"
passwords.add("thispassword")
passwords.add(sha256("thispassword"))

# 7. Row sums
row_sums = [57, 75, 74, 57, 63, 71, 25]
passwords.add(','.join(str(s) for s in row_sums))
passwords.add(''.join(str(s) for s in row_sums))
passwords.add(sha256(''.join(str(s) for s in row_sums)))
total = sum(row_sums)
passwords.add(str(total))
passwords.add(sha256(str(total)))

# 8. Matrix-specific passwords
passwords.add("matrixsumlist" + "422")
passwords.add(sha256("matrixsumlist" + "422"))
passwords.add("422matrixsumlist")
passwords.add(sha256("422matrixsumlist"))

# 9. "HASHTHETEXT" variations
passwords.add("HASHTHETEXT")
passwords.add(sha256("HASHTHETEXT"))
passwords.add("hashthetext")
passwords.add(sha256("hashthetext"))
# Hash the actual puzzle text
puzzle_text = "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
passwords.add(sha256(puzzle_text))

# 10. Try literally "lastwordsbeforearchichoice" as containing the answer
# "archi" = architect
# Last words before archi(tect's) choice = "she is going to die..."
architect_last_words = [
    "sheisgoingtodieandthereisnothingthatyoucandotostopit",
    "sheisgoingtodieandthereisnothingcanyoucandostopit",
    "sheisgoingtodieandthereisnothingicandotostopit",
    "theproblemischoice",
    "asadequatelyputtheproblemischoice",
    "wealreadyknowwhatyouaregoingto",
]
for alw in architect_last_words:
    passwords.add(alw)
    passwords.add(sha256(alw))

# 11. Maybe the answer is embedded
# "lastwordsbeforearchichoice" could be parsed as:
# "last words before arch i choice" = the last words (of the password) before making a choice
# Or: before AR(chitect)CH(oice) I = before arch-i
# Maybe it's an anagram or substitution

# 12. Previous phase passwords as keys
known_passwords = [
    "causality",
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
    "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
    "THEMATRIXHASYOU",
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",  # SHA256(causality)
    "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",  # Phase 3.1
    "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",  # Phase 3.2
]
passwords.update(known_passwords)

# 13. Try the specific hash mentioned: 89727c...
passwords.add("89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32")

# 14. Half and better half
passwords.add("halfandbetterhalf")
passwords.add(sha256("halfandbetterhalf"))
passwords.add("half and better half")

# 15. Build/construction from Issue #65
passwords.add("build")
passwords.add("BUILD")
passwords.add("starttobuild")
passwords.add("THEPUZZLEENDSWHENSTART")

# ============================================
# TEST ALL PASSWORDS
# ============================================
print(f"\nTesting {len(passwords)} unique passwords...")

count = 0
found = []

for pwd in passwords:
    count += 1
    if count % 100 == 0:
        print(f"Progress: {count}/{len(passwords)}")

    result, digest = test_password(pwd)
    if result:
        found.append((pwd, digest, result))
        print(f"\n*** FOUND READABLE OUTPUT ***")
        print(f"Password: {pwd}")
        print(f"Digest: {digest}")
        print(f"Output preview: {result[:300]}")

print(f"\n{'='*60}")
print(f"Testing complete. Found {len(found)} readable outputs.")

if found:
    with open("final_results.txt", "w") as f:
        for pwd, digest, result in found:
            f.write(f"Password: {pwd}\n")
            f.write(f"Digest: {digest}\n")
            f.write(f"Output:\n{result}\n")
            f.write("="*40 + "\n")
    print("Results saved to final_results.txt")
else:
    print("\nNo readable output found with any tested password.")
    print("\nThe puzzle remains unsolved. Possible next steps:")
    print("1. The password might use a different encoding/cipher")
    print("2. Additional clues may be needed from Decentraland or other sources")
    print("3. The decrypted output might be binary/encoded, not plaintext")
    print("4. Multi-step decryption may be required")
