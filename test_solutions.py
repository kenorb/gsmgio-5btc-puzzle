#!/usr/bin/env python3
"""
Test suite to verify all puzzle solutions match expected values
"""

import sys
from solve_puzzle import (
    sha256_hash, phase1_binary_matrix, phase3_build_password,
    phase3_2_build_password, salphaseion_hash, binary_to_ascii
)
from cipher_tools import (
    beaufort_cipher_decrypt, vic_cipher_decrypt, base10_to_base16_decode
)


# Test data constants
BINARY_SEGMENT_1 = ("a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a b b a b a a b "
                    "a b b b b a a a a b b b a a b b a b b b a b a b a b b a b b a b a b b a b b a a a "
                    "b b a b a a b a b b b a a b b a b b b a b a a")
BINARY_SEGMENT_2 = "a b b a a b a b a b b a b b b a a b b b a b a a a b b a a b a b a b b b a a b a"

HEX_SEGMENT_1 = ("a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c f d h h "
                 "c d b b c a g b d a i o b b g b e a d e d d e")
HEX_SEGMENT_2 = "c f o b f d h g d o b d g o o i i g d o c d a o o f i d h"

CHAR_MAP = {
    'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5',
    'f': '6', 'g': '7', 'h': '8', 'i': '9', 'o': '0'
}


def format_test_name(name: str) -> str:
    """Format test function name for readable output"""
    return name.replace('_', ' ').replace('test ', 'Test ').title()


def test_phase2_hash():
    """Test Phase 2 password hash"""
    expected = "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf"
    result = sha256_hash("causality")
    assert result == expected, f"Phase 2 hash mismatch: {result} != {expected}"
    print("✓ Phase 2 hash correct")


def test_phase3_hash():
    """Test Phase 3 password hash"""
    expected = "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5"
    result = phase3_build_password()
    assert result == expected, f"Phase 3 hash mismatch: {result} != {expected}"
    print("✓ Phase 3 hash correct")


def test_phase3_2_hash():
    """Test Phase 3.2 password hash"""
    expected = "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"
    result = phase3_2_build_password()
    assert result == expected, f"Phase 3.2 hash mismatch: {result} != {expected}"
    print("✓ Phase 3.2 hash correct")


def test_salphaseion_hash():
    """Test Salphaseion access hash"""
    expected = "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"
    result = salphaseion_hash()
    assert result == expected, f"Salphaseion hash mismatch: {result} != {expected}"
    print("✓ Salphaseion hash correct")


def test_binary_decode():
    """Test binary decoding"""
    expected1 = "matrixsumlist"
    result1 = binary_to_ascii(BINARY_SEGMENT_1)
    assert result1 == expected1, f"Binary 1 mismatch: {result1} != {expected1}"
    
    expected2 = "enter"
    result2 = binary_to_ascii(BINARY_SEGMENT_2)
    assert result2 == expected2, f"Binary 2 mismatch: {result2} != {expected2}"
    
    print("✓ Binary decoding correct")


def test_beaufort_cipher():
    """Test Beaufort cipher decryption"""
    key = "THEMATRIXHASYOU"
    ciphertext = "VTKVPLMEPPHLUWAHTZMJPFIPUXOHAPTUKZZTGIKFWPUYATOWYNLEBTQWFFVGAAA"
    result = beaufort_cipher_decrypt(ciphertext, key)
    expected_start = "YOURLIFEISTHESUMOFAREMAINDEROFANUNBALANCEDEQUATION"
    assert result.startswith(expected_start), f"Beaufort cipher mismatch: {result[:50]}"
    print("✓ Beaufort cipher correct")


def test_vic_cipher():
    """Test VIC cipher decryption"""
    ciphertext = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
    alphabet = "FUBCDORA.LETHINGKYMVPS.JQZXW"
    result = vic_cipher_decrypt(ciphertext, alphabet, 1, 4)
    expected_start = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHA"
    assert result.startswith(expected_start), f"VIC cipher mismatch: {result[:50]}"
    print("✓ VIC cipher correct")


def test_hex_decode():
    """Test hex decoding"""
    expected1 = "lastwordsbeforearchichoice"
    result1 = base10_to_base16_decode(HEX_SEGMENT_1, CHAR_MAP)
    assert result1 == expected1, f"Hex 1 mismatch: {result1} != {expected1}"
    
    expected2 = "thispassword"
    result2 = base10_to_base16_decode(HEX_SEGMENT_2, CHAR_MAP)
    assert result2 == expected2, f"Hex 2 mismatch: {result2} != {expected2}"
    
    print("✓ Hex decoding correct")


def test_phase1_decode():
    """Test Phase 1 binary matrix decode"""
    result = phase1_binary_matrix()
    expected = "gsmg.io/theseedisplanted"
    assert result == expected, f"Phase 1 mismatch: {result} != {expected}"
    print("✓ Phase 1 decode correct")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("RUNNING PUZZLE SOLUTION TESTS")
    print("=" * 70)
    print()
    
    tests = [
        test_phase1_decode,
        test_phase2_hash,
        test_phase3_hash,
        test_phase3_2_hash,
        test_salphaseion_hash,
        test_binary_decode,
        test_beaufort_cipher,
        test_vic_cipher,
        test_hex_decode,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {format_test_name(test.__name__)}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {format_test_name(test.__name__)}: Unexpected error: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    if failed == 0:
        print("ALL TESTS PASSED! ✓")
        print("=" * 70)
        return 0
    else:
        print(f"FAILED {failed} TEST(S)")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
