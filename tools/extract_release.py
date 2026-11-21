#!/usr/bin/env python3
"""
Fetch and decode a Qualcomm quarterly earnings release into plain text.

Qualcomm publishes its releases as PDFs that use a 2-byte CID subset font whose
low byte is offset from the real character code. Every off-the-shelf reader
returns mojibake, and this machine has no poppler (`pdftotext`/`pdftoppm`).
So we inflate the content streams ourselves, pull the text-showing operators,
and *detect* the offset rather than assuming it.

Usage:
    python3 tools/extract_release.py 2026 q4              # full decoded text
    python3 tools/extract_release.py 2026 q4 --sections   # just the blocks the model needs
    python3 tools/extract_release.py --url <pdf-url>      # if the URL pattern changes
    python3 tools/extract_release.py 2026 q4 --offset 29  # force an offset (debugging)

CID decoder uses only the standard library; standard-font SEC copies optionally
use PyPDF2. See UPDATE_RUNBOOK.md for how this fits the update cycle.
"""

import argparse
import io
import os
import re
import subprocess
import sys
import urllib.request
import zlib

# Verified for FY2025 Q4 and FY2026 Q1/Q2/Q3.
URL_TEMPLATE = ("https://s204.q4cdn.com/645488518/files/doc_financials/"
                "{fy}/{q}/FY{fy}-{ordinal}-Quarter-Earnings-Release.pdf")
ORDINALS = {"q1": "1st", "q2": "2nd", "q3": "3rd", "q4": "4th"}

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

# Tokens that must appear in a correctly decoded Qualcomm release. Used to score
# candidate offsets — this is what makes the decoder survive a font change.
EXPECTED_TOKENS = ["Qualcomm", "Revenues", "Total", "QCT", "QTL", "EBT",
                   "Fiscal", "per share", "Quarter"]

# The blocks the valuation model actually consumes. See UPDATE_RUNBOOK.md section 3.
# Needles are deliberately short: these PDFs split words across text runs
# ("QCT Revenue Strea" + "ms"), so a longer needle can miss.
SECTIONS = [
    ("Segment Results", "QCT / QTL revenue and EBT", 700),
    ("QCT Revenue Strea", "Handsets / Automotive / IoT", 460),
    # Quarterly releases say "CONDENSED CONSOLIDATED ..."; the Q4/annual one drops "CONDENSED".
    ("STATEMENTS OF OPERATIONS", "Revenue + YTD reconciliation gate", 950),
    ("Cash and cash equivalents", "Balance sheet: cash, securities, debt", 900),
    ("Depreciation and amortization", "D&A for the EBITDA bridge", 320),
    ("Current Guidance", "Next-period guidance", 600),
]


def _download(url):
    """urllib first; fall back to curl, which works where the framework Python
    has no root certificates installed (a common macOS state)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except Exception as exc:
        try:
            return subprocess.run(["curl", "-sSL", "--max-time", "60", url],
                                  check=True, stdout=subprocess.PIPE).stdout
        except (OSError, subprocess.CalledProcessError):
            sys.exit(f"error: could not download {url}\n       urllib: {exc}\n"
                     f"       curl fallback also failed.")


def fetch(url, refresh=False):
    """Download the PDF, caching it under tools/.cache/."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, url.rsplit("/", 1)[-1])
    if os.path.exists(path) and not refresh:
        with open(path, "rb") as fh:
            return fh.read(), path
    data = _download(url)
    if not data.startswith(b"%PDF"):
        sys.exit(f"error: {url} did not return a PDF (got {len(data)} bytes)")
    with open(path, "wb") as fh:
        fh.write(data)
    return data, path


def raw_strings(pdf_bytes):
    """Inflate content streams and return each shown string's raw bytes.

    Line breaks are carried as None rather than as a byte, so the offset applied
    in decode() only ever touches real glyph bytes.
    """
    chunks = []
    for m in re.finditer(rb"stream\r?\n", pdf_bytes):
        start = m.end()
        end = pdf_bytes.find(b"endstream", start)
        if end < 0:
            continue
        try:
            content = zlib.decompress(pdf_bytes[start:end])
        except zlib.error:
            continue
        if b"TJ" not in content and b"Tj" not in content:
            continue
        pieces = []
        for tm in re.finditer(rb"\((?:\\.|[^\\()])*\)|\bTd\b|\bTD\b|\bT\*\b", content):
            tok = tm.group(0)
            if tok.startswith(b"("):
                pieces.append(re.sub(rb"\\([()\\])", rb"\1", tok[1:-1]))
            else:
                pieces.append(None)          # line break
        chunks.append(pieces)
    return chunks


def decode(chunks, offset):
    """Apply the byte offset, then drop the null high bytes of the 2-byte CID encoding."""
    high = chr(offset & 0xFF)                # what a 0x00 high byte becomes
    out = []
    for pieces in chunks:
        buf = []
        for piece in pieces:
            if piece is None:
                buf.append("\n")
            else:
                buf.append("".join(chr((b + offset) & 0xFF) for b in piece).replace(high, ""))
        out.append("".join(buf))
    return "\n".join(out)


def score(text):
    """How many expected tokens appear — higher is a better-decoded candidate."""
    return sum(text.count(tok) for tok in EXPECTED_TOKENS)


def decode_auto(chunks, forced=None):
    """Find the byte offset that decodes to real English, or fail loudly."""
    candidates = [forced] if forced is not None else range(0, 64)
    scored = sorted(((score(decode(chunks, o)), o) for o in candidates), reverse=True)
    best_score, best_offset = scored[0]
    # A correct decode of a Qualcomm release hits these tokens dozens of times.
    if best_score < 20:
        print("error: could not decode this PDF — no offset produced readable text.",
              file=sys.stderr)
        print("       The font encoding has probably changed. Top candidates "
              "(score, offset):", file=sys.stderr)
        for s, o in scored[:5]:
            print(f"         {s:5}  offset {o}", file=sys.stderr)
        print("       Inspect with --offset N, or extract the figures by hand and "
              "update EXPECTED_TOKENS.", file=sys.stderr)
        sys.exit(2)
    return decode(chunks, best_offset), best_offset


def flatten(text):
    """One line per release, fields pipe-separated — how these tables read best."""
    return " | ".join(line.strip() for line in text.split("\n") if line.strip())


def print_sections(text):
    flat = flatten(text)
    missing = []
    # Standard PDF readers may split letters ("Str eams", "ST ATEMENTS").
    # Keep an index map so tolerant matching still slices the original text.
    compact_positions = [(i, c) for i, c in enumerate(flat) if not c.isspace() and c != "|"]
    compact = "".join(c for _, c in compact_positions)
    for needle, label, span in SECTIONS:
        i = flat.find(needle)
        if i < 0:
            key = "".join(c for c in needle if not c.isspace() and c != "|")
            match = compact.find(key)
            if match >= 0:
                i = compact_positions[match][0]
        if i < 0:
            missing.append(needle)
            continue
        print(f"\n{'=' * 78}\n{label}  [{needle}]\n{'=' * 78}")
        print(flat[i:i + span])
    if missing:
        print(f"\n[!] section(s) not found: {', '.join(missing)}", file=sys.stderr)
        print("    The release layout may have changed — fall back to the full "
              "text (drop --sections).", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fiscal_year", nargs="?", type=int, help="e.g. 2026")
    ap.add_argument("quarter", nargs="?", help="q1 | q2 | q3 | q4")
    ap.add_argument("--url", help="explicit PDF URL (if the naming pattern changes)")
    ap.add_argument("--sections", action="store_true",
                    help="print only the blocks the model needs")
    ap.add_argument("--offset", type=int, help="force a byte offset instead of detecting it")
    ap.add_argument("--refresh", action="store_true", help="re-download, ignoring the cache")
    args = ap.parse_args()

    if args.url:
        url = args.url
    elif args.fiscal_year and args.quarter:
        q = args.quarter.lower()
        if q not in ORDINALS:
            sys.exit(f"error: quarter must be one of {', '.join(ORDINALS)}")
        url = URL_TEMPLATE.format(fy=args.fiscal_year, q=q, ordinal=ORDINALS[q])
    else:
        ap.error("give a fiscal year and quarter (e.g. 2026 q4), or --url")

    pdf, path = fetch(url, refresh=args.refresh)
    chunks = raw_strings(pdf)
    if chunks:
        text, offset = decode_auto(chunks, forced=args.offset)
    else:
        # SEC-hosted copies may use normal fonts and content layouts that the CID
        # decoder does not handle. Never silently treat an empty decode as success.
        try:
            from PyPDF2 import PdfReader
            text = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(pdf)).pages)
        except ImportError:
            sys.exit("error: no CID text streams found. For a standard SEC PDF, install "
                     "PyPDF2>=2,<4 and retry with that Python interpreter.")
        except Exception as exc:
            sys.exit(f"error: standard PDF extraction failed: {exc}")
        if score(text) < 20:
            sys.exit("error: standard PDF extraction did not yield readable financial text")
        offset = None

    print(f"# source : {url}", file=sys.stderr)
    print(f"# cached : {path}", file=sys.stderr)
    if offset is None:
        print("# reader : PyPDF2 (standard-font PDF fallback)", file=sys.stderr)
    else:
        print(f"# offset : {offset} (auto-detected)" if args.offset is None
              else f"# offset : {offset} (forced)", file=sys.stderr)

    if args.sections:
        print_sections(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
