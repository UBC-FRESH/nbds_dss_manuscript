#!/usr/bin/env python3
"""
Abbreviate BibTeX journal titles using the ISSN LTWA list.

- Loads the official LTWA CSV (word -> abbreviation) from URL or a local path.
- Processes a .bib file entry-by-entry and updates the `journal` field:
  * If the journal appears to be a full title, replaces it with the LTWA abbreviation.
  * If the journal appears to be already abbreviated, validates tokens against LTWA;
    if non-LTWA abbreviations are detected, attempts to patch; otherwise reports.
  * Logs any pathological or ambiguous cases for manual review.

Usage:
  python scripts/abbreviate_journals.py \
    --bib references.bib \
    --out references.abbrev.bib \
    [--in-place] [--ltwa-url URL] [--ltwa-csv PATH] [--report abbrev_report.txt] \
    [--no-capitalize] [--drop-stopwords]

Notes:
  - This implements a lexicographical detection heuristic:
    A journal string is treated as an abbreviation if most tokens match LTWA
    abbreviations (or look like abbreviations, e.g., contain trailing '.') and
    no token strongly resembles a non-abbreviated, multi-letter dictionary word.
  - LTWA is a word list; there is no official full-title->abbreviation mapping.
    We therefore abbreviate titles by tokenizing into words/sub-words and mapping
    each token via LTWA where available; unknown tokens are left as-is and logged.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import requests  # type: ignore
except Exception:
    requests = None  # network-less mode supported if --ltwa-csv provided


LTWA_DEFAULT_URL = "https://www.issn.org/wp-content/uploads/2024/02/ltwa_current.csv"
ABBR_JSON_DEFAULT_URL = "https://raw.githubusercontent.com/jxhe/bib-journal-abbreviation/master/journals.json"


def _norm(s: str) -> str:
    """Unicode-insensitive, case-insensitive normalization for matching.

    - NFKD decompose accents
    - strip combining marks
    - lowercase
    - collapse extra spaces
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


@dataclass
class Ltwa:
    word_to_abbr: Dict[str, str]
    abbr_set: set
    keys_by_len: List[str]

    @classmethod
    def load(cls, csv_text: str) -> "Ltwa":
        # LTWA is tab-separated; header: WORD\tABBREVIATION\tLANGUAGES
        word_to_abbr: Dict[str, str] = {}
        abbr_set: set = set()
        reader = csv.DictReader(io.StringIO(csv_text), delimiter="\t")
        for row in reader:
            word = (row.get("WORD") or "").strip()
            abbr = (row.get("ABBREVIATION") or "").strip()
            if not word:
                continue
            # Treat trailing '-' in LTWA WORD as a root marker; remove it for matching
            word_clean = word[:-1] if word.endswith('-') else word
            nword = _norm(word_clean)
            if abbr:
                # Prefer longest root for duplicates (will be handled by keys_by_len ordering)
                # Keep first occurrence if not present yet
                word_to_abbr.setdefault(nword, abbr)
                abbr_set.add(abbr)
            else:
                # words with no abbrev are left as-is when encountered
                word_to_abbr.setdefault(nword, "")
        # Precompute keys ordered by descending length for longest-prefix match
        keys_by_len = sorted(word_to_abbr.keys(), key=len, reverse=True)
        return cls(word_to_abbr=word_to_abbr, abbr_set=abbr_set, keys_by_len=keys_by_len)


def fetch_ltwa(url: str) -> str:
    if requests is None:
        raise RuntimeError("requests not available; provide --ltwa-csv path instead")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def fetch_text(url: str) -> str:
    if requests is None:
        raise RuntimeError("requests not available; provide local file instead")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def tokenize_title(title: str) -> List[str]:
    """Split a journal title into tokens, keeping hyphenated parts separate.

    Example: "Journal of Cleaner Production" -> ["Journal", "of", "Cleaner", "Production"]
             "Bio-Resources" -> ["Bio", "-", "Resources"]
    """
    # Keep hyphens as standalone tokens, split on whitespace and punctuation except hyphen and period
    tokens: List[str] = []
    buf = ""
    for ch in title:
        if ch.isalnum() or ch in "'’&":
            buf += ch
        elif ch == '-':
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append('-')
        elif ch == '.':
            # attach period to previous token if any
            if buf:
                tokens.append(buf + '.')
                buf = ""
            elif tokens:
                tokens[-1] = tokens[-1] + '.'
        else:
            # delimiter
            if buf:
                tokens.append(buf)
                buf = ""
    if buf:
        tokens.append(buf)
    # Remove empty tokens
    return [t for t in tokens if t]


def normalize_for_title_match(s: str) -> str:
    """Normalization for matching full journal titles to JSON mapping keys.
    - lowercase
    - strip diacritics
    - replace ampersand with 'and'
    - remove extra punctuation except spaces and hyphens
    - collapse whitespace
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('&', 'and')
    s = s.lower()
    s = re.sub(r"[\.:,;()\[\]{}]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_abbreviated(journal: str, ltwa: Ltwa) -> bool:
    tokens = tokenize_title(journal)
    if not tokens:
        return False
    # Heuristics: proportion of tokens that either end with '.' or are known LTWA abbreviations
    abbrev_like = 0
    total = 0
    for tok in tokens:
        if tok == '-':
            continue
        total += 1
        if tok.endswith('.') or tok in ltwa.abbr_set:
            abbrev_like += 1
    if total == 0:
        return False
    # Consider already abbreviated if >= 60% of tokens look abbreviated
    return (abbrev_like / total) >= 0.6


STOPWORDS = {"of", "in", "and", "the"}


def cap_abbr_token(tok: str) -> str:
    # Capitalize first alphabetic character, keep rest as-is
    for i, ch in enumerate(tok):
        if ch.isalpha():
            return tok[:i] + ch.upper() + tok[i + 1 :]
    return tok


def abbreviate_title(journal: str, ltwa: Ltwa, *, capitalize: bool = True, drop_stopwords: bool = False) -> Tuple[str, List[str]]:
    """Abbreviate a journal title using LTWA word list.

    Returns (abbreviated_title, problems) where problems is a list of notes for
    tokens we could not confidently abbreviate (left as-is).
    """
    tokens = tokenize_title(journal)
    problems: List[str] = []
    out: List[str] = []
    for tok in tokens:
        if tok == '-':
            out.append('-')
            continue
        # Remove trailing period for lookup
        had_period = tok.endswith('.')
        base = tok[:-1] if had_period else tok
        nbase = _norm(base)
        # Preserve LaTeX special tokens like '&' as escaped
        if base == '&':
            out.append('\\&')
            continue
        if drop_stopwords and nbase in STOPWORDS:
            # drop token entirely
            continue
        abbr = ltwa.word_to_abbr.get(nbase)
        if abbr:
            out.append(cap_abbr_token(abbr) if capitalize else abbr)
        elif abbr == "":
            # No abbreviation per LTWA; keep as-is with normalized capitalization
            cap = base[:1].upper() + base[1:].lower()
            out.append(cap)
            problems.append(f"No LTWA abbreviation for word: '{base}' (kept as-is)")
        else:
            # Try longest-prefix match (lexicographical search) against LTWA keys
            match_abbr = None
            for k in ltwa.keys_by_len:
                if nbase.startswith(k) and ltwa.word_to_abbr.get(k):
                    match_abbr = ltwa.word_to_abbr[k]
                    break
            if match_abbr:
                out.append(cap_abbr_token(match_abbr) if capitalize else match_abbr)
            else:
                # Not found in LTWA: keep token as-is (title case) and log
                cap = base[:1].upper() + base[1:].lower()
                out.append(cap)
                problems.append(f"Word not found in LTWA: '{base}' (kept as-is)")
        # Ensure periods on abbreviations per LTWA are already present; do not add extra
    # Recombine, managing spaces around hyphens cleanly
    abbr_title = []
    for i, t in enumerate(out):
        if t == '-':
            if abbr_title and abbr_title[-1].endswith(' '):
                abbr_title[-1] = abbr_title[-1].rstrip()
            abbr_title.append('-')
        else:
            if abbr_title and abbr_title[-1] != '-':
                abbr_title.append(' ')
            abbr_title.append(t)
    result = ''.join(abbr_title).replace(' -', '-').replace('- ', '-')
    return result, problems


def validate_abbreviation(journal: str, ltwa: Ltwa) -> Tuple[bool, List[str]]:
    """Validate that each token in an already abbreviated title is a valid LTWA abbreviation.

    Returns (is_valid, issues)
    """
    tokens = tokenize_title(journal)
    issues: List[str] = []
    valid_parts = 0
    total_parts = 0
    for tok in tokens:
        if tok == '-':
            continue
        total_parts += 1
        if tok in ltwa.abbr_set:
            valid_parts += 1
        elif tok.endswith('.'):
            # Looks like an abbreviation but not recognized by LTWA
            issues.append(f"Token not in LTWA abbreviations: '{tok}'")
        else:
            # Likely not abbreviated token in an abbreviated title
            issues.append(f"Non-abbreviated token in abbreviated title: '{tok}'")
    is_valid = (valid_parts == total_parts)
    return is_valid, issues


@dataclass
class EntryUpdate:
    key: str
    original: str
    updated: str
    action: str  # 'replaced', 'validated', 'patched', 'skipped', 'error'
    notes: List[str]


def load_abbr_json(text: str) -> Dict[str, str]:
    import json
    raw = json.loads(text)
    mapping: Dict[str, str] = {}
    for full, abbr in raw.items():
        k = normalize_for_title_match(full)
        # Prefer first occurrence for stability
        mapping.setdefault(k, abbr)
    return mapping


def process_bib_text(
    bib_text: str,
    ltwa: Ltwa,
    *,
    capitalize: bool = True,
    drop_stopwords: bool = False,
    abbr_map: Optional[Dict[str, str]] = None,
) -> Tuple[str, List[EntryUpdate]]:
    """Parse BibTeX text, update journal fields, and return updated text and log."""
    updates: List[EntryUpdate] = []

    def split_entries(text: str) -> List[str]:
        entries: List[str] = []
        i = 0
        n = len(text)
        while i < n:
            at = text.find('@', i)
            if at == -1:
                break
            # copy any preamble before entry
            j = at
            # find matching closing '}' for this entry
            depth = 0
            k = j
            started = False
            while k < n:
                ch = text[k]
                if ch == '{':
                    depth += 1
                    started = True
                elif ch == '}':
                    depth -= 1
                    if started and depth == 0:
                        k += 1
                        break
                k += 1
            if k <= j:
                # malformed; bail out
                entries.append(text[j:])
                break
            entries.append(text[j:k])
            i = k
        # Append trailing text (if any) as-is
        if i < n:
            tail = text[i:]
            if tail.strip():
                entries.append(tail)
        return entries

    entry_texts = split_entries(bib_text)
    updated_entries: List[str] = []

    key_re = re.compile(r"^@[^\{]+\{\s*([^,]+)", re.S)

    for raw in entry_texts:
        mkey = key_re.search(raw)
        key = mkey.group(1).strip() if mkey else "?"
        # search for journal field
        def find_and_replace_journal(entry_text: str) -> Tuple[str, Optional[EntryUpdate]]:
            # Locate 'journal =' and parse value (handles nested braces or quotes)
            m = re.search(r"(?im)\bjournal\s*=", entry_text)
            if not m:
                return entry_text, None
            start = m.end()
            # Skip whitespace
            i = start
            n = len(entry_text)
            while i < n and entry_text[i].isspace():
                i += 1
            if i >= n:
                return entry_text, None
            opener = entry_text[i]
            if opener not in '{"':
                return entry_text, None
            val_start = i + 1
            if opener == '"':
                # find closing unescaped quote
                j = val_start
                while j < n:
                    if entry_text[j] == '"' and entry_text[j - 1] != '\\':
                        break
                    j += 1
                val_end = j
                closer = '"'
            else:
                # braces with depth
                depth = 1
                j = val_start
                while j < n and depth > 0:
                    ch = entry_text[j]
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                    j += 1
                val_end = j - 1  # position of matching '}'
                closer = '}'
            original_val = entry_text[val_start:val_end]
            trailing = ''
            # Build updated journal value
            notes: List[str] = []
            try:
                if is_abbreviated(original_val, ltwa):
                    valid, issues = validate_abbreviation(original_val, ltwa)
                    if valid:
                        upd = EntryUpdate(key, original_val, original_val, 'validated', [])
                        return entry_text, upd
                    else:
                        notes.extend(issues)
                        upd = EntryUpdate(key, original_val, original_val, 'skipped', notes)
                        return entry_text, upd
                else:
                    # First try exact JSON mapping if provided
                    if abbr_map is not None:
                        lookup_key = normalize_for_title_match(original_val)
                        abbr_json = abbr_map.get(lookup_key)
                        if abbr_json:
                            # Ensure LaTeX-escaped ampersand in abbreviation
                            abbr_fixed = abbr_json.replace('&', '\\&')
                            new_val = abbr_fixed
                            new_text = (
                                entry_text[:val_start] + new_val + entry_text[val_end:]
                            )
                            upd = EntryUpdate(key, original_val, new_val, 'replaced', ["via json mapping"])
                            return new_text, upd
                    # Fallback to LTWA algorithm
                    abbr, probs = abbreviate_title(original_val, ltwa, capitalize=capitalize, drop_stopwords=drop_stopwords)
                    notes.extend(probs)
                    if abbr != original_val:
                        new_val = abbr
                        new_text = (
                            entry_text[:val_start] + new_val + entry_text[val_end:]
                        )
                        upd = EntryUpdate(key, original_val, new_val, 'replaced', notes)
                        return new_text, upd
                    else:
                        upd = EntryUpdate(key, original_val, original_val, 'skipped', notes)
                        return entry_text, upd
            except Exception as e:
                upd = EntryUpdate(key, original_val, original_val, 'error', [str(e)])
                return entry_text, upd

        new_raw, upd = find_and_replace_journal(raw)
        if upd is not None:
            updates.append(upd)
        updated_entries.append(new_raw)

    # Ensure entries are separated by blank lines for readability
    out_text = "\n\n".join(e.strip() for e in updated_entries) + "\n"
    return out_text, updates


def format_report(updates: Sequence[EntryUpdate]) -> str:
    lines: List[str] = []
    counts = {}
    for u in updates:
        counts[u.action] = counts.get(u.action, 0) + 1
    lines.append("Abbreviation report")
    lines.append("===================")
    lines.append("Summary:")
    for k in sorted(counts):
        lines.append(f"  {k}: {counts[k]}")
    lines.append("")
    for u in updates:
        lines.append(f"Entry: {u.key}")
        lines.append(f"  Action: {u.action}")
        lines.append(f"  Original: {u.original}")
        lines.append(f"  Updated:  {u.updated}")
        if u.notes:
            lines.append("  Notes:")
            for n in u.notes:
                lines.append(f"    - {n}")
        lines.append("")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Abbreviate BibTeX journal titles using LTWA")
    p.add_argument("--bib", type=Path, default=Path("references.bib"), help="Input .bib file")
    p.add_argument("--out", type=Path, default=Path("references.abbrev.bib"), help="Output .bib file")
    p.add_argument("--in-place", action="store_true", help="Overwrite input file in place")
    p.add_argument("--ltwa-url", default=LTWA_DEFAULT_URL, help="URL to LTWA CSV (default: official)")
    p.add_argument("--ltwa-csv", type=Path, help="Local path to LTWA CSV (skip network)")
    p.add_argument("--abbr-json", type=Path, help="Local path to full-title→abbrev JSON mapping")
    p.add_argument("--abbr-json-url", default=ABBR_JSON_DEFAULT_URL, help="URL to full-title→abbrev JSON mapping")
    p.add_argument("--report", type=Path, default=Path("abbrev_report.txt"), help="Report output path")
    p.add_argument("--no-capitalize", action="store_true", help="Do not capitalize LTWA abbreviations (default: capitalize)")
    p.add_argument("--drop-stopwords", action="store_true", help="Drop common stopwords (of, in, and, the) from journal titles")
    args = p.parse_args(argv)

    if args.ltwa_csv and args.ltwa_csv.exists():
        csv_text = args.ltwa_csv.read_text(encoding="utf-8", errors="ignore")
    else:
        try:
            csv_text = fetch_ltwa(args.ltwa_url)
        except Exception as e:
            print(f"Error fetching LTWA CSV: {e}", file=sys.stderr)
            return 2

    ltwa = Ltwa.load(csv_text)

    bib_text = args.bib.read_text(encoding="utf-8", errors="ignore")
    # Load optional JSON abbreviation map
    abbr_map = None
    try:
        if args.abbr_json and args.abbr_json.exists():
            abbr_map = load_abbr_json(args.abbr_json.read_text(encoding="utf-8", errors="ignore"))
        else:
            # Try fetching from URL but ignore errors silently
            try:
                txt = fetch_text(args.abbr_json_url)
                abbr_map = load_abbr_json(txt)
            except Exception:
                abbr_map = None
    except Exception as e:
        print(f"Warning: failed to load abbreviation JSON: {e}", file=sys.stderr)
        abbr_map = None

    updated_text, updates = process_bib_text(
        bib_text,
        ltwa,
        capitalize=not args.no_capitalize,
        drop_stopwords=args.drop_stopwords,
        abbr_map=abbr_map,
    )

    if args.in_place:
        args.out = args.bib
    args.out.write_text(updated_text, encoding="utf-8")

    report = format_report(updates)
    args.report.write_text(report, encoding="utf-8")

    # Print brief summary to stdout
    print("Wrote:", args.out)
    print("Report:", args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
