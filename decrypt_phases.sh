#!/bin/bash
# GSMG.IO 5 BTC Puzzle Decryption Helper
# This script helps decrypt the encrypted phases of the puzzle

set -e

echo "========================================================================"
echo "GSMG.IO 5 BTC PUZZLE - DECRYPTION HELPER"
echo "========================================================================"
echo ""

# Phase 2 decryption
echo "[PHASE 2] Causality decryption"
echo "Password: causality"
PHASE2_HASH=$(echo -n "causality" | sha256sum | cut -d' ' -f1)
echo "SHA256: $PHASE2_HASH"
echo ""
echo "To decrypt phase2.txt, run:"
echo "  openssl enc -aes-256-cbc -d -a -in phase2.txt -pass pass:$PHASE2_HASH"
echo ""

# Phase 3 decryption
echo "[PHASE 3] Multi-part password"
PHASE3_CONCAT="causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1"
PHASE3_HASH=$(echo -n "$PHASE3_CONCAT" | sha256sum | cut -d' ' -f1)
echo "SHA256: $PHASE3_HASH"
echo ""
echo "To decrypt phase3.txt, run:"
echo "  openssl enc -aes-256-cbc -d -a -in phase3.txt -pass pass:$PHASE3_HASH"
echo ""

# Phase 3.2 decryption
echo "[PHASE 3.2] Second multi-part password"
PHASE3_2_CONCAT="jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
PHASE3_2_HASH=$(echo -n "$PHASE3_2_CONCAT" | sha256sum | cut -d' ' -f1)
echo "SHA256: $PHASE3_2_HASH"
echo ""
echo "To decrypt phase3.2.txt, run:"
echo "  openssl enc -aes-256-cbc -d -a -in phase3.2.txt -pass pass:$PHASE3_2_HASH"
echo ""

# Salphaseion access
echo "[SALPHASEION] Access URL"
SALPHASEION_TEXT="GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
SALPHASEION_HASH=$(echo -n "$SALPHASEION_TEXT" | sha256sum | cut -d' ' -f1)
echo "SHA256: $SALPHASEION_HASH"
echo "URL: https://gsmg.io/$SALPHASEION_HASH"
echo ""

echo "========================================================================"
echo "Decryption commands generated successfully!"
echo "========================================================================"
