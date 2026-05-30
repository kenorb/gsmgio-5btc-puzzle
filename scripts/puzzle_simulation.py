#!/usr/bin/env python3
"""Generate an HTML report that simulates the GSMG.IO puzzle steps."""

from __future__ import annotations

import dataclasses
import hashlib
import html
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclasses.dataclass
class ChecklistItem:
    title: str
    status: str = "pending"
    details: List[str] = dataclasses.field(default_factory=list)
    children: List["ChecklistItem"] = dataclasses.field(default_factory=list)

    def mark(self, status: str, detail: str | None = None) -> None:
        self.status = status
        if detail:
            self.details.append(detail)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_bits(bits: str, size: int = 8) -> List[str]:
    return [bits[i : i + size] for i in range(0, len(bits), size)]


def bits_to_ascii(bits: Iterable[str]) -> str:
    chars = []
    for block in bits:
        if len(block) != 8:
            continue
        chars.append(chr(int(block, 2)))
    return "".join(chars)


def spiral_counterclockwise(matrix: List[List[int]]) -> List[int]:
    top, left = 0, 0
    bottom, right = len(matrix) - 1, len(matrix[0]) - 1
    result: List[int] = []

    while top <= bottom and left <= right:
        # down
        for row in range(top, bottom + 1):
            result.append(matrix[row][left])
        left += 1
        if left > right:
            break
        # right
        for col in range(left, right + 1):
            result.append(matrix[bottom][col])
        bottom -= 1
        if top > bottom:
            break
        # up
        for row in range(bottom, top - 1, -1):
            result.append(matrix[row][right])
        right -= 1
        if left > right:
            break
        # left
        for col in range(right, left - 1, -1):
            result.append(matrix[top][col])
        top += 1
    return result


def abba_to_ascii(text: str) -> str:
    bits = text.replace(" ", "").replace("a", "0").replace("b", "1")
    return bits_to_ascii(chunk_bits(bits, 8))


def a_i_o_to_ascii(text: str) -> Tuple[str, str, str]:
    mapping = {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8", "i": "9", "o": "0"}
    digits = "".join(mapping[ch] for ch in text.split())
    as_int = int(digits)
    as_hex = format(as_int, "x")
    if len(as_hex) % 2 == 1:
        as_hex = "0" + as_hex
    decoded = bytes.fromhex(as_hex).decode("utf-8", errors="replace")
    return digits, as_hex, decoded


def sanitize_printable(data: bytes) -> Tuple[str, bool]:
    text = data.decode("utf-8", errors="replace")
    printable = sum(ch.isprintable() for ch in text)
    ratio = printable / max(len(text), 1)
    return text, ratio > 0.9


def try_openssl_decrypt(blob: str, password: str) -> Tuple[str, bool, str]:
    with subprocess.Popen(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-d",
            "-a",
            "-A",
            "-pass",
            f"pass:{password}",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        stdout, stderr = proc.communicate(blob.encode("utf-8"), timeout=10)
    text, is_printable = sanitize_printable(stdout)
    return text, is_printable, stderr.decode("utf-8", errors="replace").strip()


def main() -> None:
    start_time = time.perf_counter()
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "puzzle_simulation.html"

    matrix = [
        [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    ]

    spiral_bits = "".join(str(bit) for bit in spiral_counterclockwise(matrix))
    spiral_bytes = chunk_bits(spiral_bits)
    spiral_message = bits_to_ascii(spiral_bytes)

    abba_matrixsumlist = (
        "a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a "
        "b b a b a a b a b b b b a a a a b b b a a b b a b b b a b a b a b "
        "b a b b a b a b b a b b a a a b b a b a a b a b b b a a b b a b b "
        "b a b a a"
    )
    abba_enter = "a b b a a b a b a b b a b b b a a b b b a b a a a b b a a b a b a b b b a a b a"

    matrixsumlist = abba_to_ascii(abba_matrixsumlist)
    enter_text = abba_to_ascii(abba_enter)

    lastwords_input = (
        "a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c "
        "f d h h c d b b c a g b d a i o b b g b e a d e d d e"
    )
    thispassword_input = "c f o b f d h g d o b d g o o i i g d o c d a o o f i d h"

    lastwords_digits, lastwords_hex, lastwords_text = a_i_o_to_ascii(lastwords_input)
    thispassword_digits, thispassword_hex, thispassword_text = a_i_o_to_ascii(thispassword_input)

    sha_values = {
        "causality": sha256_hex("causality"),
        "matrixsumlist": sha256_hex(matrixsumlist),
        "enter": sha256_hex(enter_text),
        "matrixsumlistenter": sha256_hex(matrixsumlist + enter_text),
        "lastwordsbeforearchichoice": sha256_hex(lastwords_text),
        "thispassword": sha256_hex(thispassword_text),
        "theseedisplanted": sha256_hex("theseedisplanted"),
    }

    phase3_password = (
        "causality"
        "Safenet"
        "Luna"
        "HSM"
        "11110"
        "0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854"
        "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1"
    )
    phase3_hash = sha256_hex(phase3_password)

    phase32_password = "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple"
    phase32_hash = sha256_hex(phase32_password)

    aes_blob = (
        "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
        "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
    )

    candidates = [
        ("matrixsumlist", sha_values["matrixsumlist"]),
        ("enter", sha_values["enter"]),
        ("matrixsumlistenter", sha_values["matrixsumlistenter"]),
        ("lastwordsbeforearchichoice", sha_values["lastwordsbeforearchichoice"]),
        ("thispassword", sha_values["thispassword"]),
        ("theseedisplanted", sha_values["theseedisplanted"]),
        ("causality", sha_values["causality"]),
        ("phase3_hash", phase3_hash),
        ("phase32_hash", phase32_hash),
    ]

    decrypt_attempts = []
    for label, key in candidates:
        try:
            text, printable, stderr = try_openssl_decrypt(aes_blob, key)
        except Exception as exc:  # noqa: BLE001 - report errors
            decrypt_attempts.append((label, key, False, f"error: {exc}"))
            continue
        if printable:
            summary = text.strip()[:200]
            outcome = f"printable: {summary}"
        else:
            outcome = stderr or "non-printable output"
        decrypt_attempts.append((label, key, printable, outcome))

    checklist = ChecklistItem(
        "Puzzle simulation checklist",
        children=[
            ChecklistItem(
                "Phase 1: Spiral decode",
                children=[
                    ChecklistItem("Build matrix"),
                    ChecklistItem("Spiral traversal"),
                    ChecklistItem("ASCII decode"),
                ],
            ),
            ChecklistItem(
                "Phase 2: Hidden form password",
                children=[
                    ChecklistItem("Record password string"),
                    ChecklistItem("Compute SHA256 for causality"),
                ],
            ),
            ChecklistItem(
                "Phase 3: AES setup",
                children=[
                    ChecklistItem("Compute phase 3 concatenated hash"),
                    ChecklistItem("Compute phase 3.2 hash"),
                ],
            ),
            ChecklistItem(
                "Salphaseion: decode and attempt AES",
                children=[
                    ChecklistItem("Decode ABBA strings"),
                    ChecklistItem("Decode a-i-o numeric text"),
                    ChecklistItem("Attempt AES blob candidates"),
                ],
            ),
        ],
    )

    checklist.children[0].children[0].mark("done", "Matrix loaded")
    checklist.children[0].children[1].mark("done", f"Bits collected: {len(spiral_bits)}")
    checklist.children[0].children[2].mark("done", f"Message: {spiral_message}")

    checklist.children[1].children[0].mark("done", "Password recorded from hint")
    checklist.children[1].children[1].mark("done", f"SHA256(causality)={sha_values['causality']}")

    checklist.children[2].children[0].mark("done", f"SHA256(phase3 concat)={phase3_hash}")
    checklist.children[2].children[1].mark("done", f"SHA256(phase3.2)={phase32_hash}")

    checklist.children[3].children[0].mark("done", f"ABBA decode: {matrixsumlist}, {enter_text}")
    checklist.children[3].children[1].mark("done", f"a-i-o decode: {lastwords_text}, {thispassword_text}")
    checklist.children[3].children[2].mark(
        "done" if any(item[2] for item in decrypt_attempts) else "partial",
        "AES attempts completed",
    )

    def render_checklist(item: ChecklistItem) -> str:
        status_emoji = {"done": "✅", "partial": "⚠️", "pending": "⬜"}.get(item.status, "⬜")
        details = "".join(f"<li class='detail'>{html.escape(detail)}</li>" for detail in item.details)
        children = "".join(render_checklist(child) for child in item.children)
        return (
            "<li>"
            f"<span class='status'>{status_emoji}</span> "
            f"<span class='title'>{html.escape(item.title)}</span>"
            f"<ul class='details'>{details}</ul>"
            f"<ul class='children'>{children}</ul>"
            "</li>"
        )

    spiral_preview = " ".join(spiral_bytes[:20])
    runtime_seconds = time.perf_counter() - start_time
    report_html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>GSMG Puzzle Simulation Report</title>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 32px; color: #222; }}
    h1, h2, h3 {{ color: #1f3b73; }}
    code, pre {{ background: #f4f7fb; padding: 2px 4px; border-radius: 4px; }}
    pre {{ padding: 12px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d1d8e0; padding: 8px; text-align: left; }}
    th {{ background: #eef2f7; }}
    .status {{ margin-right: 8px; }}
    ul.details {{ margin: 6px 0 6px 24px; color: #4a5568; }}
    ul.children {{ margin-left: 20px; }}
    .card {{ border: 1px solid #d9e1f2; padding: 16px; border-radius: 8px; margin-bottom: 18px; }}
  </style>
</head>
<body>
  <h1>GSMG.IO Puzzle Simulation Report</h1>
  <p>Generated: {datetime.now(timezone.utc).isoformat()}</p>

  <div class="card">
    <h2>Checklist</h2>
    <ul class="checklist">{render_checklist(checklist)}</ul>
    <p><strong>Run time:</strong> {runtime_seconds:.2f}s across {len(decrypt_attempts)} AES attempts.</p>
  </div>

  <div class="card">
    <h2>Phase 1: Spiral Decode</h2>
    <p><strong>Spiral bits (preview):</strong> {html.escape(spiral_preview)} ...</p>
    <p><strong>Decoded message:</strong> <code>{html.escape(spiral_message)}</code></p>
    <p><strong>SHA256(gsmg.io/theseedisplanted):</strong> {sha256_hex('gsmg.io/theseedisplanted')}</p>
  </div>

  <div class="card">
    <h2>Phase 2: Hidden Form &amp; Hash</h2>
    <p>Password from hint: <code>theflowerblossomsthroughwhatseemstobeaconcretesurface</code></p>
    <p>SHA256(causality): <code>{sha_values['causality']}</code></p>
  </div>

  <div class="card">
    <h2>Phase 3: AES Preparation</h2>
    <p>Concatenated password hash:</p>
    <pre>{phase3_hash}</pre>
    <p>Phase 3.2 hash:</p>
    <pre>{phase32_hash}</pre>
  </div>

  <div class="card">
    <h2>Salphaseion Decoding</h2>
    <p><strong>ABBA decoded:</strong> {matrixsumlist} / {enter_text}</p>
    <p><strong>Numeric decode:</strong></p>
    <ul>
      <li>Digits: {lastwords_digits}</li>
      <li>Hex: {lastwords_hex}</li>
      <li>Text: {lastwords_text}</li>
    </ul>
    <ul>
      <li>Digits: {thispassword_digits}</li>
      <li>Hex: {thispassword_hex}</li>
      <li>Text: {thispassword_text}</li>
    </ul>
  </div>

  <div class="card">
    <h2>AES Blob Attempts (Experimental)</h2>
    <table>
      <thead>
        <tr><th>Candidate</th><th>Key</th><th>Printable?</th><th>Outcome</th></tr>
      </thead>
      <tbody>
        {''.join(f"<tr><td>{html.escape(label)}</td><td><code>{key}</code></td><td>{'✅' if printable else '⚠️'}</td><td>{html.escape(outcome)}</td></tr>" for label, key, printable, outcome in decrypt_attempts)}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Next-Step Experiment Notes</h2>
    <ul>
      <li>Evaluate alternate interpretations of <code>matrixsumlist</code> as a matrix operation.</li>
      <li>Try combined keys (matrixsumlist + enter + lastwordsbeforearchichoice).</li>
      <li>Brute-force variants of Matrix quotes from the Architect scene.</li>
      <li>Search for additional keys hinted by "sha256 ans too".</li>
    </ul>
  </div>
</body>
</html>
"""

    report_path.write_text(report_html, encoding="utf-8")
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    main()
