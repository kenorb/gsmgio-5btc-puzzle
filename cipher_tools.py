#!/usr/bin/env python3
"""
Advanced Cipher Tools for GSMG.IO Puzzle
Implements VIC cipher and Beaufort cipher decryption
"""

def vic_cipher_decrypt(ciphertext: str, alphabet: str, digit1: int, digit2: int) -> str:
    """
    Decrypt VIC cipher
    
    Args:
        ciphertext: Numeric ciphertext string
        alphabet: Custom alphabet (e.g., "FUBCDORA.LETHINGKYMVPS.JQZXW")
        digit1: First digit for VIC cipher
        digit2: Second digit for VIC cipher
    
    Returns:
        Decrypted plaintext
    """
    # VIC cipher uses a straddling checkerboard
    # This is a simplified implementation
    
    # Create the checkerboard based on digits
    checkerboard = {}
    
    # First row (0-9, excluding digit1 and digit2)
    row0_positions = [i for i in range(10) if i not in [digit1, digit2]]
    for i, pos in enumerate(row0_positions):
        if i < len(alphabet):
            checkerboard[str(pos)] = alphabet[i]
    
    # Second row (digit1 prefix)
    offset = len(row0_positions)
    for i in range(10):
        idx = offset + i
        if idx < len(alphabet):
            checkerboard[f"{digit1}{i}"] = alphabet[idx]
    
    # Third row (digit2 prefix)
    offset = len(row0_positions) + 10
    for i in range(10):
        idx = offset + i
        if idx < len(alphabet):
            checkerboard[f"{digit2}{i}"] = alphabet[idx]
    
    # Decrypt the ciphertext
    result = []
    i = 0
    while i < len(ciphertext):
        # Try two-digit code first
        if i + 1 < len(ciphertext):
            two_digit = ciphertext[i:i+2]
            if two_digit in checkerboard:
                result.append(checkerboard[two_digit])
                i += 2
                continue
        
        # Try one-digit code
        one_digit = ciphertext[i]
        if one_digit in checkerboard:
            result.append(checkerboard[one_digit])
            i += 1
        else:
            result.append(ciphertext[i])
            i += 1
    
    return ''.join(result)


def beaufort_cipher_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt Beaufort cipher
    Beaufort cipher: P = K - C (mod 26)
    
    Args:
        ciphertext: Encrypted text
        key: Decryption key
    
    Returns:
        Decrypted plaintext
    """
    key = key.upper()
    ciphertext = ciphertext.upper()
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            c = ord(char) - ord('A')
            k = ord(key[key_index % len(key)]) - ord('A')
            p = (k - c) % 26
            result.append(chr(p + ord('A')))
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def base10_to_base16_decode(text: str, char_map: dict) -> str:
    """
    Convert custom base-10 representation to base-16 and decode as hex
    Used in Salphaseion phase
    
    Args:
        text: Text with custom digits (e.g., using a-i, o for 0-9)
        char_map: Mapping of characters to digits
    
    Returns:
        Decoded ASCII text
    """
    # Convert to actual digits
    digits = ''.join(char_map.get(c, c) for c in text.replace(' ', ''))
    
    # Validate input length to prevent memory issues
    if len(digits) > 1000:
        return f"Input too long: {len(digits)} digits (max 1000)"
    
    # Convert from base 10 to base 16
    try:
        # Treat as base-10 number and convert to hex
        hex_value = hex(int(digits))[2:]  # Remove '0x' prefix
        
        # Decode hex to ASCII with explicit error handling
        try:
            result = bytes.fromhex(hex_value).decode('ascii')
            return result
        except UnicodeDecodeError as e:
            # Use replace to show problematic characters instead of hiding them
            result = bytes.fromhex(hex_value).decode('ascii', errors='replace')
            return f"{result} (Warning: Non-ASCII characters replaced)"
    except ValueError as e:
        return f"Decoding error: {e}"


def main():
    """Test the cipher implementations"""
    print("=" * 70)
    print("ADVANCED CIPHER TOOLS TEST")
    print("=" * 70)
    
    # Test Beaufort cipher
    print("\n[TEST 1] Beaufort Cipher")
    test_cipher = "VTKVPLMEPPHLUWAHTZMJPFIPUXOHAPTUKZZTGIKFWPUYATOWYNLEBTQWFFVGAAA"
    key = "THEMATRIXHASYOU"
    decrypted = beaufort_cipher_decrypt(test_cipher, key)
    print(f"Ciphertext: {test_cipher[:50]}...")
    print(f"Key: {key}")
    print(f"Decrypted: {decrypted[:50]}...")
    
    # Test VIC cipher
    print("\n[TEST 2] VIC Cipher")
    vic_ciphertext = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
    vic_alphabet = "FUBCDORA.LETHINGKYMVPS.JQZXW"
    vic_decrypted = vic_cipher_decrypt(vic_ciphertext, vic_alphabet, 1, 4)
    print(f"Ciphertext: {vic_ciphertext[:50]}...")
    print(f"Alphabet: {vic_alphabet}")
    print(f"Digits: 1, 4")
    print(f"Decrypted: {vic_decrypted[:50]}...")
    
    # Test base conversion
    print("\n[TEST 3] Salphaseion Hex Decode")
    char_map = {
        'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
        'f': '6', 'g': '7', 'h': '8', 'i': '9', 'o': '0'
    }
    test_hex = "a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c f d h h c d b b c a g b d a i o b b g b e a d e d d e"
    decoded_hex = base10_to_base16_decode(test_hex, char_map)
    print(f"Input: {test_hex[:50]}...")
    print(f"Decoded: {decoded_hex}")
    
    test_hex2 = "c f o b f d h g d o b d g o o i i g d o c d a o o f i d h"
    decoded_hex2 = base10_to_base16_decode(test_hex2, char_map)
    print(f"Input: {test_hex2}")
    print(f"Decoded: {decoded_hex2}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
