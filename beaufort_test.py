#!/usr/bin/env python3
"""
GSMG.IO Puzzle - Beaufort Cipher Testing
Try Beaufort cipher on blob with THEMATRIXHASYOU
"""

import base64
import hashlib
import subprocess

# The SalPhaselon AES blob
BLOB_BASE64 = """U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z
QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"""

def beaufort_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt using Beaufort cipher"""
    result = []
    key = key.upper()
    key_len = len(key)
    key_idx = 0

    for char in ciphertext.upper():
        if char.isalpha():
            # Beaufort: P = K - C (mod 26)
            c_val = ord(char) - ord('A')
            k_val = ord(key[key_idx % key_len]) - ord('A')
            p_val = (k_val - c_val) % 26
            result.append(chr(p_val + ord('A')))
            key_idx += 1
        else:
            result.append(char)

    return ''.join(result)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt using Vigenere cipher"""
    result = []
    key = key.upper()
    key_len = len(key)
    key_idx = 0

    for char in ciphertext.upper():
        if char.isalpha():
            c_val = ord(char) - ord('A')
            k_val = ord(key[key_idx % key_len]) - ord('A')
            p_val = (c_val - k_val) % 26
            result.append(chr(p_val + ord('A')))
            key_idx += 1
        else:
            result.append(char)

    return ''.join(result)

def try_as_text():
    """Try decoding blob as direct text and apply ciphers"""
    blob_raw = base64.b64decode(BLOB_BASE64.replace('\n', ''))

    # Extract just alphabetic characters
    alpha_chars = ''.join(chr(b) for b in blob_raw if 65 <= b <= 90 or 97 <= b <= 122)
    print(f"Alphabetic chars in blob: {alpha_chars[:100]}...")

    # Try Beaufort with THEMATRIXHASYOU
    keys_to_try = [
        "THEMATRIXHASYOU",
        "MATRIXHASYOU",
        "THEMATRIX",
        "MATRIX",
        "CAUSALITY",
        "CHOICE",
        "ARCHITECT",
        "NEO",
        "TRINITY",
        "MORPHEUS",
        "ORACLE",
        "MATRIXSUMLIST",
        "ENTER",
    ]

    for key in keys_to_try:
        beaufort_result = beaufort_decrypt(alpha_chars, key)
        vigenere_result = vigenere_decrypt(alpha_chars, key)

        print(f"\nKey: {key}")
        print(f"Beaufort: {beaufort_result[:80]}...")
        print(f"Vigenere: {vigenere_result[:80]}...")

# The long cipher text from phase 3.2.1 that was decoded with Beaufort
PHASE321_CIPHER = """vtkvplmepphluwahtzmjpfipuxohaptukzztgikfwpuyatowynlebtqwffvgaaaxjflrxvokligooxeiexjywwukuucdlfwpwekogsngbvtzmnteulhpuchmrabiiejptvcaqbspqauhpmdjqhaqhuyddiwgxvxgpofaqizsentyesqmgchuazmyhmnrbzioyhucvqzcfmwxotomoblfeblcngppselsnlwaehcnwxznaynaceazhfzeunpeewjvhjysqjpposalabzuaplpppteafvvnzpryhsnkjuxsmkubnnimopukojensnlfxfabgeujmyqbqwtnmzitbtqwukuwfnxmfpepxuiwuxqqvgwgpzpptnguyaloavsnkppuhohkcazrghmrpbhicegsjdntttepqdmzrkdbstiabnasjmytghqhimcadgjvlhuvqaaababytxqhetvnpsknbinpxxwzrkfczjmhphezjmydkqtqrixlyhdolhuocpoecwakafomluodaoxmhxkiehekgkituelmynbpuhovoblpiyjakbduxbulpfnntcfmpqdsfdkcavazhakiepelyvabbkoitycfvushkbcjwzuadivfmgjdmbawzhmnekelhuocpykuhmnxiniregjqzlenbyexemnpucaleeiajvrjmyhdmodleopqkqnnzqbootnqmcybmdiajxmrdmmnqybgtllqkcizuihmjqpviehxwatlipitudotsfqgzmakmhnpqzinyxtzogygigvtmwbtghlpxttpgifohsgempkpiyatudomayqtzwtutlymtwppubmtwwuhmnwjphdhkrlflmzinushphruituniiedvfdirevdpplmibxrtehlqwylwtzmaqeeawhywbazsismrntewafxgvdbmjpzpmdiagaaihrjsmrntgwqkcqpkciwqjvrwcotjmrzazhtyaeototuhrowynfmpqdceegcgtitmcnpdqnzkvnppqsjrngjewaydjflwzutyelsmbyxwqzmuwhjvxoselapaaakmqnkjntejkpzwtoytarzqwklwqcowzuakeiqsgunubzcuaoyegltkwhwfniepiqegdkyqxqqoquwingecjemazpqlqwgykeajoummeaavibjledwfubscjptsfeqxuxehwqydrenanrelsfulftpmqmcoqetvkllbmdekhzrxiqsxyvqjdgzmanpqhhsnwgsqktwodrvznmmgomodijpbopqwptominnihfpulspucgbmoxeieauvdiacgjiqaugiyakhysfosijmasrzkfowgwxubauepijvrjmyhsmiwpyepamqzylwaaewajelybeawobvqcvwzaajuktvukudxztbhfgacdafvsmiwkbhlfiedpuhkczwlenaketkhklmbltryvaketuhkhkhppmyvvdogpwhtwqicyymqgovxnodkdaaabwbzagdahnqnfsaomzaeeawelkslhqlwigij"""

def try_salphaselon_letters():
    """Try deciphering the letter grid from SalPhaselon"""
    # The letter grid from SalPhaselon (lowercase a-i letters, o=0)
    letter_grid = """d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e f a e d g g e e d f c b d a b h h g g c a d c f e d d g f d g b g i g a a e d g g i a f a e c g h g g c d a i h e h a h b a h i g c e i f g b f g e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c"""

    # Clean up
    letters = letter_grid.replace(' ', '').replace('\n', '')
    print(f"Total letters: {len(letters)}")
    print(f"First 100: {letters[:100]}")

    # Convert a-i to 1-9, o to 0
    def letters_to_digits(s):
        mapping = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'o': '0'}
        return ''.join(mapping.get(c, c) for c in s)

    digits = letters_to_digits(letters)
    print(f"\nAs digits: {digits[:100]}...")

    # Try as row sums (from the puzzle)
    # Reshape into rows and calculate sums
    # The grid seems to be 7 rows based on sums 57, 75, 74, 57, 63, 71, 25

    # Try different interpretations
    # 1. Direct sum of all digits
    total_sum = sum(int(d) for d in digits if d.isdigit())
    print(f"\nTotal sum of all digits: {total_sum}")

    # 2. As a number in various bases
    try:
        # Base 9+1 interpretation
        digit_num = int(digits[:50], 10)  # First 50 as decimal
        print(f"First 50 as decimal: {digit_num}")
        print(f"As hex: {hex(digit_num)}")
    except:
        pass

    # 3. Try affine cipher (from Issue #51)
    # P = 2(C-8) mod 9
    def affine_decrypt(digits_str):
        result = []
        for d in digits_str:
            if d.isdigit():
                c = int(d)
                if c == 0:
                    c = 10  # Treat 0 as 10 for mod 9
                p = (2 * (c - 8)) % 9
                result.append(str(p))
        return ''.join(result)

    affine_result = affine_decrypt(digits)
    print(f"\nAffine decrypted (first 100): {affine_result[:100]}")

def test_passwords_from_findings():
    """Test passwords based on new findings"""
    passwords = [
        # From Issue #65
        "SUMREMAINDERUNBALANCEDEQUATION",
        "sumremainderunbalancedequation",
        "SUMREMAINDER",
        "sumremainder",
        "UNBALANCEDEQUATION",
        "unbalancedequation",
        "YOUARETHESUM",
        "youarethesum",
        "YOUARESUMREMAINDER",
        "yourlifeisthesumofaRemainderofanunbalancedequation",
        "yourlifeisthesumofaremainderofanunbalancedequation",

        # From decoded phase 3.2.1
        "YOURLIFEISTHESUMOFREMAINDERUNBALANCEDEQUATION",
        "remainderofunbalancedequation",
        "systemicanomaly",
        "anomalyinharmany",
        "mathematicalprecision",

        # The Beaufort decoded message mentioned "TWENTY-THREE CIPHERS, SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS"
        "23",
        "16",
        "7",
        "twentythreesixteenseven",
        "23167",
        "71623",

        # From Issue #55 - the key that was used
        "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23",

        # Build/construction theme from Issue #65
        "build",
        "BUILD",
        "THEPUZZLEENDSWHENSTART",
        "starttobuild",
        "constructiong",
    ]

    print("\n" + "="*60)
    print("Testing new passwords from research findings")
    print("="*60)

    for pwd in passwords:
        for digest in ["", "-md md5", "-md sha256"]:
            cmd = f'openssl enc -aes-256-cbc -d -a {digest} -in salphaselon_blob.txt -pass "pass:{pwd}" 2>/dev/null'
            result = subprocess.run(cmd, shell=True, capture_output=True)
            if result.returncode == 0:
                output = result.stdout
                printable = sum(1 for b in output if 32 <= b <= 126 or b in [9, 10, 13])
                if len(output) > 0 and printable / len(output) > 0.7:
                    print(f"\n*** POTENTIAL HIT ***")
                    print(f"Password: {pwd}")
                    print(f"Digest: {digest}")
                    print(f"Output: {output[:200]}")

if __name__ == "__main__":
    print("="*60)
    print("GSMG.IO Puzzle - Beaufort and Cipher Testing")
    print("="*60)

    print("\n--- Testing Beaufort on blob characters ---")
    try_as_text()

    print("\n--- Analyzing SalPhaselon letter grid ---")
    try_salphaselon_letters()

    print("\n--- Testing passwords from findings ---")
    test_passwords_from_findings()
