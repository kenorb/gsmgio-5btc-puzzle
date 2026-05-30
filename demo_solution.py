#!/usr/bin/env python3
"""
GSMG.IO 5 BTC Puzzle - Complete Demonstration
This script demonstrates solving all known phases of the puzzle
"""

import sys
from solve_puzzle import (
    sha256_hash, phase1_binary_matrix, phase3_build_password,
    phase3_2_build_password, salphaseion_hash, binary_to_ascii
)
from cipher_tools import (
    beaufort_cipher_decrypt, vic_cipher_decrypt, base10_to_base16_decode
)


def demonstrate_phase1():
    """Demonstrate Phase 1 solution"""
    print("\n" + "=" * 70)
    print("PHASE 1: Binary Matrix Decoding")
    print("=" * 70)
    print("\nChallenge: https://gsmg.io/puzzle")
    print("Task: Decode 14x14 binary matrix (black/blue=1, yellow/white=0)")
    print("\nMethod: Read spiral counterclockwise from top-left, convert to ASCII")
    
    result = phase1_binary_matrix()
    print(f"\n✓ Decoded URL path: {result}")
    print(f"  Full URL: https://gsmg.io/{result}")


def demonstrate_phase2():
    """Demonstrate Phase 2 solution"""
    print("\n" + "=" * 70)
    print("PHASE 2: The Warning")
    print("=" * 70)
    print("\nChallenge: https://gsmg.io/theseedisplanted")
    print("Task: Find password and decrypt AES content")
    
    print("\nClues:")
    print("  - Images reference 'The Warning' by Logic (war+ning, LO+gic)")
    print("  - Hidden form password hint from song lyrics")
    print("  - Decryption key from Matrix quote: 'causality'")
    
    password = "causality"
    pwd_hash = sha256_hash(password)
    
    print(f"\n✓ Password: {password}")
    print(f"  SHA256: {pwd_hash}")
    print("\nDecrypt command:")
    print(f"  openssl enc -aes-256-cbc -d -a -in phase2.txt \\")
    print(f"    -pass pass:{pwd_hash}")


def demonstrate_phase3():
    """Demonstrate Phase 3 solution"""
    print("\n" + "=" * 70)
    print("PHASE 3: Multi-Part Password")
    print("=" * 70)
    print("\nTask: Concatenate 7 parts and decrypt")
    
    print("\nParts:")
    print("  1. causality (from Phase 2)")
    print("  2. Safenet (Thales HSM reference)")
    print("  3. Luna (Thales Luna HSM)")
    print("  4. HSM (Hardware Security Module)")
    print("  5. 11110 (JFK Executive Order 11110)")
    print("  6. 0x736B6E... (Genesis block hex data)")
    print("  7. B5KR/1r5B... (Chess position after 'buddhist move')")
    
    pwd_hash = phase3_build_password()
    print(f"\n✓ Password SHA256: {pwd_hash}")
    print("\nDecrypt command:")
    print(f"  openssl enc -aes-256-cbc -d -a -in phase3.txt \\")
    print(f"    -pass pass:{pwd_hash}")


def demonstrate_phase3_2():
    """Demonstrate Phase 3.2 solution"""
    print("\n" + "=" * 70)
    print("PHASE 3.2: Philosophical Password")
    print("=" * 70)
    print("\nTask: Build password from philosophical/literary references")
    
    print("\nParts:")
    print("  1. jacquefresco - 'the future is ours' quote")
    print("  2. giveitjustonesecond - Alice in Wonderland reference")
    print("  3. heisenbergsuncertaintyprinciple - Physics principle")
    
    pwd_hash = phase3_2_build_password()
    print(f"\n✓ Password SHA256: {pwd_hash}")
    print("\nDecrypt command:")
    print(f"  openssl enc -aes-256-cbc -d -a -in phase3.2.txt \\")
    print(f"    -pass pass:{pwd_hash}")


def demonstrate_phase3_2_1():
    """Demonstrate Phase 3.2.1 Beaufort cipher"""
    print("\n" + "=" * 70)
    print("PHASE 3.2.1: Beaufort Cipher")
    print("=" * 70)
    print("\nTask: Decrypt Beaufort cipher with Matrix reference key")
    
    print("\nClues:")
    print("  - 'I've designed you a beautiful strategic position'")
    print("  - beautiful -> Beaufort cipher")
    print("  - 'Why am I here? Wake up, Neo. The matrix has you'")
    
    key = "THEMATRIXHASYOU"
    sample_cipher = "VTKVPLMEPPHLUWAHTZMJPFIPUXOHAPTUKZZTGIKFWPUYATOWYNLEBTQWFFVGAAA"
    decrypted = beaufort_cipher_decrypt(sample_cipher, key)
    
    print(f"\n✓ Key: {key}")
    print(f"  Sample ciphertext: {sample_cipher[:40]}...")
    print(f"  Decrypted: {decrypted[:40]}...")
    print("\n  Full message reveals private key retrieval complexity:")
    print("  - 23+ ciphers")
    print("  - 16+ encryptions")
    print("  - 7+ intertwined passwords")


def demonstrate_phase3_2_2():
    """Demonstrate Phase 3.2.2 VIC cipher"""
    print("\n" + "=" * 70)
    print("PHASE 3.2.2: VIC Cipher")
    print("=" * 70)
    print("\nTask: Decrypt VIC cipher with custom alphabet")
    
    print("\nClues:")
    print("  - 'A fubcd-king & oracle-queen, thingky mvps'")
    print("  - Extract unique letters: FUBCDORA.LETHINGKYMVPS")
    print("  - 'one for one, four for one' -> digits 1 and 4")
    
    ciphertext = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
    alphabet = "FUBCDORA.LETHINGKYMVPS.JQZXW"
    decrypted = vic_cipher_decrypt(ciphertext, alphabet, 1, 4)
    
    print(f"\n✓ Alphabet: {alphabet}")
    print(f"  Digits: 1, 4")
    print(f"  Ciphertext: {ciphertext[:40]}...")
    print(f"  Decrypted: {decrypted[:50]}...")


def demonstrate_salphaseion():
    """Demonstrate Salphaseion phase"""
    print("\n" + "=" * 70)
    print("SALPHASEION / COSMIC DUALITY PHASE")
    print("=" * 70)
    print("\nTask: Access hidden phase via hashed text")
    
    print("\nClue:")
    print("  'Go back to the first puzzle piece without further ado'")
    print("  Hash the text from the first page")
    
    text = "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
    hash_value = salphaseion_hash()
    
    print(f"\n✓ Text: {text}")
    print(f"  SHA256: {hash_value}")
    print(f"  URL: https://gsmg.io/{hash_value}")
    
    # Binary segments
    print("\nBinary decoding (a=0, b=1):")
    binary1 = "a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a b b a b a a b a b b b b a a a a b b b a a b b a b b b a b a b a b b a b b a b a b b a b b a a a b b a b a a b a b b b a a b b a b b b a b a a"
    result1 = binary_to_ascii(binary1)
    print(f"  Segment 1: {result1}")
    
    binary2 = "a b b a a b a b a b b a b b b a a b b b a b a a a b b a a b a b a b b b a a b a"
    result2 = binary_to_ascii(binary2)
    print(f"  Segment 2: {result2}")
    
    # Hex-encoded segments
    print("\nHex-encoded segments (a=1...i=9, o=0):")
    char_map = {
        'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
        'f': '6', 'g': '7', 'h': '8', 'i': '9', 'o': '0'
    }
    
    hex1 = "a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c f d h h c d b b c a g b d a i o b b g b e a d e d d e"
    decoded1 = base10_to_base16_decode(hex1, char_map)
    print(f"  Segment 3: {decoded1}")
    
    hex2 = "c f o b f d h g d o b d g o o i i g d o c d a o o f i d h"
    decoded2 = base10_to_base16_decode(hex2, char_map)
    print(f"  Segment 4: {decoded2}")


def demonstrate_additional_hints():
    """Show additional puzzle hints"""
    print("\n" + "=" * 70)
    print("ADDITIONAL HINTS")
    print("=" * 70)
    
    print("\n1. Decentraland Audio Clue:")
    print("   - Find audio at specific coordinates")
    print("   - Process: Split stereo, invert, mix, spectrogram")
    print("   - Result: HASHTHETEXT")
    
    print("\n2. Hidden Poem Clue:")
    print("   'Roses are White but often Red.")
    print("    Yellow has a number and so does Blue.")
    print("    Go back to the first puzzle piece without further ado.'")
    print("   -> Leads to Salphaseion phase")
    
    print("\n3. Prize Information:")
    print("   - Address: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")
    print("   - Original: 5 BTC")
    print("   - Current: 2.5 BTC (after halving on May 11, 2020)")
    print("   - Creator's note: Prize meant for meaningful blockchain work")


def main():
    """Main demonstration"""
    print("\n" + "=" * 70)
    print("          GSMG.IO 5 BTC PUZZLE - COMPLETE SOLUTION")
    print("=" * 70)
    print("\nThis demonstration shows all known solutions to the puzzle phases.")
    print("Note: The final private key extraction remains extremely complex.")
    
    demonstrate_phase1()
    demonstrate_phase2()
    demonstrate_phase3()
    demonstrate_phase3_2()
    demonstrate_phase3_2_1()
    demonstrate_phase3_2_2()
    demonstrate_salphaseion()
    demonstrate_additional_hints()
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("\nAll documented phases have been solved and automated.")
    print("The final stage requires solving:")
    print("  - 23+ different ciphers")
    print("  - 16+ encryption layers")
    print("  - 7+ intertwined passwords")
    print("  - Potential brute force attacks")
    print("\nThe puzzle creator warns this is intentionally extremely difficult.")
    print("Scripts in this repository automate all known solution steps.")
    print("\n" + "=" * 70)
    print("\nAvailable tools:")
    print("  ./solve_puzzle.py     - Main solver with all hash generation")
    print("  ./cipher_tools.py     - Beaufort, VIC, and hex decoding tools")
    print("  ./decrypt_phases.sh   - Generate OpenSSL decryption commands")
    print("  ./demo_solution.py    - This comprehensive demonstration")
    print("=" * 70)


if __name__ == "__main__":
    main()
