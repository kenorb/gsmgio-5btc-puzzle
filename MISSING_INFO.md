# Missing Information in GSMG.IO 5 BTC Puzzle

This document catalogs gaps, inconsistencies, and undecrypted elements in the puzzle documentation.

---

## 1. Undecrypted AES Blobs

### Phase 3.2.1 AES Blob (README lines 285-287)
```
U2FsdGVkX1+0Wl49gnWTyiimluu7V3+vl7st0gUt9sWDzNLxDmlPMsDSiuW2a46z
gKlIi8aaqY5gpJPPEzW1n9n3/26qs4zstWtPKF8Zs/BTNN4IiEh4qu18mdC0NAv4
```
**Status:** Password UNKNOWN
**Context:** Appears after Beaufort cipher decryption, before VIC cipher section
**Possible passwords to try:**
- Derived from "HASHTHETEXT" hint
- Related to the VIC cipher output
**Tested (2026-06-XX):**
- SHA256 of the Beaufort plaintext paragraph (`216411b7026a3661134f4dcc140d49b0b3599b683ed2afa837ab3ef4244597ba`) → **bad decrypt**

### Cosmic Duality AES Blob Discrepancy
**README has (spaced):**
```
U 2 F s d G V k X 1 8 6 t Y U 0 h V J B X X U n B U O 7 C 0 + X 4 K U W n W k C v o Z S x b R D 3 w N s G W V H e f v d r d 9 z
Q v X 0 t 8 v 3 j P B 4 o k p s p x e b R i 6 s E 1 B M l 5 H I 8 R k u + K e j U q T v d W O X 6 n Q j S p e p X w G u N / j J
```

**Image (SalPhaselonCosmicDuality.png) shows DIFFERENT blob:**
```
U2FsdGVkX18tP2/gbc1Q5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFe
dGJh4SJIP66qRtXvo7PtpvsIjw08prLiC/sNHthxiGMuqIrKo0224rOisFJZgARi
c7PaJPne4nab8XCFuV3NbfxGX2BUjNkef5hg7nsoadZx08dNyU2b6eiciWiUvu7D
SATSFO7IFBiAMz7dDqIETKuG1TAP4EmMQUZrQNtfbJsURATW6V5VSbtzB5RFk0O+
IymhstzrQHsU0Bugjv2nndmOEhCxGi/1qK2rLNdOOLutYGnA6RDDbFJUattggELh
2SZx+SBpCdbSGjxOap2719FOy1o2r0HU6UxFdcsbfZ1utTqVEyNs91emQxtppt+6
BPZisi1743v4EmrpRDC3ufnkmlwR8NfqVPIKhUiGDu5Qf1YjczT6DrA9vLQZu3bk
k+/ZurtRYnqqsj49UhwEF9GFuF17uQYm0UunatW43C3Z1tyFRGAzAHQUFS6jRCd+
vZGyoT1OsThJXDDCSAwoX2M+yH+oaEQoVVDuWvKIqRhfDNuBmEfi+HpXuJLPBS1Pb
...
```
**Status:** This is a DIFFERENT encrypted blob than what's documented
**Action needed:** Verify which is correct and determine password

---

## 2. Unsolved Formula: X 2 S H 4 Y 0 Q B 15

From Phase 2 decryption (README line 114):
```
# X 2 S H 4 Y 0 Q B 15 #
```

### Known Values:
| Symbol | Clue | Decoded Value |
|--------|------|---------------|
| S | Klingon: cha' + (vagh * jav) = 2+(5*6) | **32** |
| B | (BV80605001911AP - sqrt(-1))² = (5i-i)² = (4i)² | **-16** |
| Q | "extend the name of a hacker's swordless fish, the I and W are below" | **Unknown** (Blowfish?) |
| H | "(Answer to only this puzzle but nothing else) * -1" | **Unknown** |

### Unknown Values:
- **X** - Not explained
- **2** - Position marker or value?
- **4** - Position marker or value?
- **Y** - Not explained
- **0** - Position marker or value?
- **15** - Not explained

### Questions:
1. Is this a substitution cipher key?
2. Is it a formula to compute something?
3. What does "the I and W are below" mean for Q?

---

## 3. SalPhaseion Decoded Elements - Incomplete Usage

### Decoded strings:
1. **"matrixsumlist"** - How is this used?
2. **"enter"** - Command or password component?
3. **"lastwordsbeforearchichoice"** - What are the last words before Archi's choice?
4. **"thispassword"** - What password does this refer to?

### Undecoded hint:
```
sha b e f our first hint is your last command
sha b e ef ans too
```
- If shabef = sha256 (b=2, e=5, f=6), what is the "last command"?
- What does "ans too" decode to?

---

## 4. Colored Letters in SalPhaselon Grid

The image shows letters a-i with different colors (blue, red/orange, green, yellow, etc.).

**Missing from documentation:**
- What do the colors signify?
- Is there a pattern to extract?
- Do colored letters form a separate message?

---

## 5. Phase 3 Hint: "_green_ came _back_"

From phase3.png:
> "Years later the idea of this _green_ came _back_"

**Questions:**
- What does the underscore notation mean?
- Is "green" a reference to something specific?
- Bitcoin genesis block reference? (Satoshi?)

---

## 6. HASHTHETEXT - Decentraland Hint

**Source:** Audio file at Decentraland coordinates (-41, -17)
**Answer:** HASHTHETEXT

**Unresolved:**
- Which text should be hashed?
- What hash algorithm?
- Where should the result be used?

---

## 7. "23 Ciphers, 16 Encryptions, 7 Passwords"

From Phase 3.2.1 Beaufort decryption:
> "you will be required to select from over TWENTY-THREE CIPHERS, SIXTEEN ENCRYPTIONS and or SEVEN INTERTWINED PASSWORDS"

**Documented so far:**
- AES-256-CBC (multiple instances)
- Beaufort cipher
- VIC cipher
- SHA-256 hashing
- Binary to ASCII
- Hex to ASCII
- Base64 encoding
- IBM EBCDIC 1141 encoding
- a1z26 cipher

**Missing:** Many more ciphers/encryptions are implied but not documented.

---

## 8. Roses Hint - Incomplete Interpretation

```
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.
```

**Partially solved:** Led to hashing "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

**Unresolved:**
- "Yellow has a number" - What number?
- "Blue has a number" - What number?
- Are these referring to the colored squares in the original 14x14 matrix?

---

## 9. Private Key Location

The VIC cipher decryption reveals:
> "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"

**Questions:**
- Who/what is "half and better half"?
- Does this mean the private key is split?
- Is there a multi-signature wallet involved?

---

## 10. Chess Position Verification

**Initial position (from puzzle):**
```
B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1
```

**After buddhist move:**
```
B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1
```

**The move:** Rook from g6 to c6 (6R1 → 2R5)

**Verify:** Is this the only non-mate move? Are there alternatives?

---

## 11. Numerical Motif Clue (3-6-9, 137, π)

Community chatter repeatedly cites "magical" numbers (3-6-9, 1-3-7, pi) but their role is undocumented.

**Questions:**
- Should these digits be appended/prepended to known strings (e.g., `matrixsumlist137`, `enter314159`)?
- Are they offsets when reading the SalPhaselon grid (every 3rd/6th/9th cell)?
- Do SHA256 hashes of these constants unlock any AES blobs?

---

## Summary Table

| Item | Status | Priority |
|------|--------|----------|
| Phase 3.2.1 AES blob | Undecrypted | HIGH |
| Cosmic Duality blob discrepancy | Needs verification | HIGH |
| Numerical motifs (3-6-9, 137, π) | Untested | MEDIUM |
| X 2 S H 4 Y 0 Q B 15 formula | Partially decoded | MEDIUM |
| SalPhaseion decoded strings usage | Unknown | HIGH |
| Colored letter significance | Undocumented | MEDIUM |
| "_green_ came _back_" clue | Unexplained | LOW |
| HASHTHETEXT application | Unknown | MEDIUM |
| Remaining ciphers/encryptions | Undocumented | HIGH |
| Roses hint numbers | Incomplete | LOW |
| Private key split mechanism | Unknown | HIGH |

---

## Next Steps for Puzzle Solvers

1. **Verify the Cosmic Duality AES blob** - Compare README vs image content
2. **Attempt decryption of Phase 3.2.1 blob** with candidate passwords:
   - "HASHTHETEXT"
   - Combinations of decoded SalPhaseion strings
   - VIC cipher output variations
3. **Analyze colored letters** in SalPhaselon grid for hidden message
4. **Research "lastwordsbeforearchichoice"** - possibly Matrix Reloaded scene?
5. **Complete the X 2 S H 4 Y 0 Q B 15 formula** decoding
