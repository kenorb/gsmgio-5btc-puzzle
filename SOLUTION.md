# GSMG.IO 5 BTC Puzzle - Complete Solution Guide

This document provides a complete solution guide for the GSMG.IO 5 BTC puzzle challenge with working scripts and tools.

## Overview

The GSMG.IO 5 BTC puzzle is a multi-phase cryptographic challenge with a prize of 5 BTC (reduced to 2.5 BTC after Bitcoin halving on May 11, 2020).

- **Prize Address**: [1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe](https://www.blockchain.com/btc/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)
- **Puzzle URL**: https://gsmg.io/puzzle

## Solution Tools

This repository now includes automated solution tools:

### 1. `solve_puzzle.py` - Python Solver Script
A comprehensive Python script that implements all the decryption logic:
- Phase 1: Binary matrix decoding
- Phase 2: Causality password generation
- Phase 3: Multi-part password concatenation
- Phase 3.2: Secondary password generation
- Salphaseion: Access hash generation
- Beaufort cipher utilities

**Usage:**
```bash
python3 solve_puzzle.py
```

### 2. `decrypt_phases.sh` - Bash Decryption Helper
A bash script that generates the OpenSSL commands needed to decrypt each phase:

**Usage:**
```bash
./decrypt_phases.sh
```

## Complete Solution Walkthrough

### Phase 1: Binary Matrix Decoding
**Challenge**: https://gsmg.io/puzzle  
**Task**: Decode a 14x14 binary matrix (black/blue = '1', yellow/white = '0')

**Solution**:
1. Read the matrix in a counterclockwise spiral from top-left
2. Convert 8-bit sequences to ASCII characters
3. Result: `gsmg.io/theseedisplanted`

**Automated**: Run `solve_puzzle.py` to decode automatically

### Phase 2: The Warning
**Challenge**: https://gsmg.io/theseedisplanted  
**Password**: `theflowerblossomsthroughwhatseemstobeaconcretesurface`

**Decryption**:
1. The hidden form password is derived from the song "The Warning" by Logic
2. After submitting, you get encrypted AES content
3. Key: SHA256("causality") = `eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf`

**Decrypt with**:
```bash
openssl enc -aes-256-cbc -d -a -in phase2.txt -pass pass:eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
```

### Phase 3: Multi-Part Password
**Challenge**: Concatenate 7 parts and decrypt

**Parts**:
1. `causality` (from Phase 2)
2. `Safenet` (Thales Hardware Security Module)
3. `Luna` (Thales Luna HSM)
4. `HSM` (Hardware Security Module)
5. `11110` (JFK Executive Order 11110)
6. `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854` (Genesis block raw data)
7. `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1` (Chess position)

**Password Hash**: SHA256 of concatenated parts = `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`

**Decrypt with**:
```bash
openssl enc -aes-256-cbc -d -a -in phase3.txt -pass pass:1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

### Phase 3.2: Philosophical Password
**Parts**:
1. `jacquefresco` (Jacque Fresco: "the future is ours")
2. `giveitjustonesecond` (Alice: "How long is forever?" / White Rabbit: "Sometimes, just one second")
3. `heisenbergsuncertaintyprinciple` (Fundamental physics principle)

**Password Hash**: SHA256 = `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`

**Decrypt with**:
```bash
openssl enc -aes-256-cbc -d -a -in phase3.2.txt -pass pass:250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

#### Phase 3.2.1: Beaufort Cipher
**Key**: `THEMATRIXHASYOU`  
**Algorithm**: Beaufort cipher decryption  
**Decoded message**: Instructions about the private key and warnings about complexity

#### Phase 3.2.2: VIC Cipher
**Alphabet**: `FUBCDORA.LETHINGKYMVPS.JQZXW`  
**Digits**: 1, 4  
**Result**: "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"

### Salphaseion / Cosmic Duality Phase
**Access**: SHA256("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")  
**Hash**: `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`  
**URL**: https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32

**Binary segments**:
- `abbaabba...` (a=0, b=1) decodes to: `matrixsumlist`
- Second segment decodes to: `enter`

**Hex-encoded messages** (using mapping a=1...i=9, o=0):
- Segment 1: `lastwordsbeforearchichoice`
- Segment 2: `thispassword`

**Final decryption**: Still partially unsolved - involves 23 ciphers, 16 encryptions, and 7 intertwined passwords

## Additional Hints

### Decentraland Audio Hint
**Location**: Specific coordinates in Decentraland  
**Process**: 
1. Get audio file from coordinates
2. Split stereo track, invert one channel
3. Mix back together, mono conversion
4. Create spectrogram
**Result**: `HASHTHETEXT`

### Hidden Hints
From the puzzle creator:
```
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.
```

This leads to hashing the text on the first puzzle page, which opens the Salphaseion phase.

## Key Insights

1. **Matrix References**: The puzzle heavily references The Matrix trilogy
2. **Layered Encryption**: Multiple layers of AES-256-CBC with SHA256 password hashing
3. **Cryptographic Knowledge**: Requires understanding of various cipher types
4. **Cultural References**: Movies, songs, chess, physics, historical events
5. **Complexity Warning**: The creator warns the final stage is extremely difficult

## Current Status

The puzzle is documented up to Phase 3.2 with partial solutions for Salphaseion. The final private key extraction involves:
- 23+ different ciphers
- 16+ encryption layers
- 7+ intertwined passwords
- Possible brute forcing required

## Usage Instructions

1. **Run the solver**:
   ```bash
   python3 solve_puzzle.py
   ```

2. **Generate decryption commands**:
   ```bash
   ./decrypt_phases.sh
   ```

3. **Create encrypted phase files** (if you have the encrypted content from the website):
   - Save encrypted content to `phase2.txt`, `phase3.txt`, `phase3.2.txt`
   - Run the OpenSSL commands from `decrypt_phases.sh`

## Notes

- The puzzle prize address still contains 2.5 BTC as of the last check
- The creator intended this to promote blockchain technology development
- The final message suggests the prize should fund meaningful work, not just treasure hunting
- Some phases may require accessing the actual https://gsmg.io website for encrypted content

## Credits

This solution compiles publicly available information from:
- Reddit discussions on r/bitcoinpuzzles
- Community contributions and pull requests
- The GSMG.IO puzzle website

## Disclaimer

This is an educational resource documenting a public cryptographic puzzle. The solutions are derived from publicly available information and community efforts.
