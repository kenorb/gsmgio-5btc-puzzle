#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Analyze the SalPhaselon letter grid
Try to find the meaning of "matrixsumlist"
"""

import hashlib
import subprocess

# The letter grid from the SalPhaselon image (extracted)
# First few rows from the image:
# d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e

# Full grid (approximately, from image reading)
LETTER_GRID = """
d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e
g g e c b e d c i b f b f f g i g b e e e
e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c
"""

def clean_grid(grid_text):
    """Extract just the letters a-i from the grid"""
    return [c for c in grid_text.lower() if c in 'abcdefghi']

def letters_to_digits(letters):
    """Convert letters a-i to digits 1-9"""
    return [ord(c) - ord('a') + 1 for c in letters]

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def test_password(password):
    """Test password"""
    cmd = f'openssl enc -aes-256-cbc -d -a -in salphaselon_blob.txt -pass "pass:{password}" 2>/dev/null'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode == 0 and len(result.stdout) > 0:
        output = result.stdout
        printable = sum(1 for b in output if 32 <= b <= 126 or b in [9, 10, 13])
        if printable / len(output) > 0.7:
            return output.decode('utf-8', errors='replace')
    return None

# Clean the grid
letters = clean_grid(LETTER_GRID)
digits = letters_to_digits(letters)

print(f"Total letters: {len(letters)}")
print(f"First 20 letters: {''.join(letters[:20])}")
print(f"First 20 as digits: {digits[:20]}")

# ========================================
# COMPUTE VARIOUS SUMS
# ========================================
print("\n=== Various Sum Calculations ===")

# Total sum
total_sum = sum(digits)
print(f"Total sum: {total_sum}")
print(f"Total sum as binary: {bin(total_sum)[2:]}")
print(f"Total sum as hex: {hex(total_sum)}")

# Try as password
passwords_to_try = []
passwords_to_try.append(str(total_sum))
passwords_to_try.append(bin(total_sum)[2:])
passwords_to_try.append(hex(total_sum)[2:])

# If we interpret as a 7-row grid (from known row sums 57,75,74,57,63,71,25)
# Let's try to reshape into rows
if len(digits) >= 100:
    # Try different row lengths
    for row_len in [10, 12, 14, 16, 18, 20]:
        rows = [digits[i:i+row_len] for i in range(0, len(digits), row_len)]
        row_sums = [sum(row) for row in rows]
        print(f"\nRow length {row_len}: first 7 row sums = {row_sums[:7]}")

        # Check if matches known sums
        known_sums = [57, 75, 74, 57, 63, 71, 25]
        if row_sums[:7] == known_sums:
            print("*** MATCHES KNOWN ROW SUMS! ***")

        # Add various formats as passwords
        passwords_to_try.append(','.join(str(s) for s in row_sums[:7]))
        passwords_to_try.append(''.join(str(s) for s in row_sums[:7]))
        passwords_to_try.append(sha256(''.join(str(s) for s in row_sums[:7])))

# Try digits as a number and convert to hex then ASCII
digit_str = ''.join(str(d) for d in digits[:60])  # First 60 digits
print(f"\nFirst 60 digits as string: {digit_str}")

# Try base-10 to hex to ASCII conversion
try:
    as_int = int(digit_str[:20])
    print(f"First 20 as decimal: {as_int}")
    print(f"As hex: {hex(as_int)}")
except:
    pass

# ========================================
# THE SPECIFIC DECODING FROM README
# ========================================
# From README: using a=1..i=9, o=0, then converting to base 16, then hex-to-ASCII
# Example: 174161018595377387932283725836301293648834223172419022725145445 → lastwordsbeforearchichoice

print("\n=== Trying README decoding method ===")

# The grid before separators contains the encoded messages
# Let's look for the specific encoded strings

# From the image/README:
# agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobggbeadedde → lastwordsbeforearchichoice
# cfobfdhgdobdgooiigdocdaoofidh → thispassword

encoded1 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobgbeadedde"
encoded2 = "cfobfdhgdobdgooiigdocdaoofidh"

def decode_to_number(text):
    """Convert a-i to 1-9, o to 0"""
    mapping = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6',
               'g': '7', 'h': '8', 'i': '9', 'o': '0'}
    return ''.join(mapping.get(c, c) for c in text)

def decode_to_ascii(encoded):
    """Full decoding: letters -> digits -> base16 -> hex -> ASCII"""
    digits = decode_to_number(encoded)
    print(f"Digits: {digits}")
    try:
        # Convert to base 16
        decimal = int(digits)
        hex_str = hex(decimal)[2:]
        print(f"Hex: {hex_str}")
        # Convert hex to ASCII
        if len(hex_str) % 2 == 1:
            hex_str = '0' + hex_str
        ascii_result = bytes.fromhex(hex_str).decode('ascii', errors='replace')
        return ascii_result
    except Exception as e:
        print(f"Error: {e}")
        return None

print("\nDecoding encoded1:")
result1 = decode_to_ascii(encoded1)
print(f"Result: {result1}")

print("\nDecoding encoded2:")
result2 = decode_to_ascii(encoded2)
print(f"Result: {result2}")

# ========================================
# TEST PASSWORDS
# ========================================
print("\n=== Testing various sum passwords ===")

# Add more passwords based on decoded elements
if result1:
    passwords_to_try.append(result1)
    passwords_to_try.append(sha256(result1))
if result2:
    passwords_to_try.append(result2)
    passwords_to_try.append(sha256(result2))

# Try the actual decoded messages
passwords_to_try.extend([
    "lastwordsbeforearchichoice",
    "thispassword",
    sha256("lastwordsbeforearchichoice"),
    sha256("thispassword"),
    "lastwordsbeforearchichoicethispassword",
    sha256("lastwordsbeforearchichoicethispassword"),
])

# Unique passwords
passwords_to_try = list(set(passwords_to_try))

print(f"\nTesting {len(passwords_to_try)} password variations...")
for pwd in passwords_to_try:
    result = test_password(pwd)
    if result:
        print(f"\n*** FOUND ***")
        print(f"Password: {pwd}")
        print(f"Result: {result[:200]}")

print("\nDone!")
