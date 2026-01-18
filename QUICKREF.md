# Quick Reference Guide

## Running the Solution Scripts

### Main Solver
Generates all passwords and hashes for each phase:
```bash
python3 solve_puzzle.py
```

### Cipher Tools
Tests Beaufort cipher, VIC cipher, and hex decoding:
```bash
python3 cipher_tools.py
```

### Decryption Helper
Generates OpenSSL commands for decrypting puzzle phases:
```bash
./decrypt_phases.sh
```

### Complete Demonstration
Shows a comprehensive walkthrough of all solutions:
```bash
python3 demo_solution.py
```

## Key Hashes

### Phase 2
- Password: `causality`
- SHA256: `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf`

### Phase 3
- Combined parts SHA256: `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`

### Phase 3.2
- Combined parts SHA256: `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`

### Salphaseion
- Access hash: `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`

## Decryption Commands

### Decrypt Phase 2
```bash
openssl enc -aes-256-cbc -d -a -in phase2.txt \
  -pass pass:eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
```

### Decrypt Phase 3
```bash
openssl enc -aes-256-cbc -d -a -in phase3.txt \
  -pass pass:1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

### Decrypt Phase 3.2
```bash
openssl enc -aes-256-cbc -d -a -in phase3.2.txt \
  -pass pass:250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

## Cipher Keys

### Beaufort Cipher (Phase 3.2.1)
- Key: `THEMATRIXHASYOU`

### VIC Cipher (Phase 3.2.2)
- Alphabet: `FUBCDORA.LETHINGKYMVPS.JQZXW`
- Digits: 1, 4

## URLs

- Puzzle start: https://gsmg.io/puzzle
- Phase 2: https://gsmg.io/theseedisplanted
- Salphaseion: https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32
- Prize address: https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe

## Script Dependencies

All scripts require Python 3.x. No external Python packages needed - uses only standard library:
- `hashlib` for SHA256
- `subprocess` for OpenSSL calls
- `base64` for encoding (built-in)

For OpenSSL decryption commands, you need `openssl` installed:
```bash
# Ubuntu/Debian
sudo apt-get install openssl

# macOS
brew install openssl

# Windows
# Download from https://slproweb.com/products/Win32OpenSSL.html
```
