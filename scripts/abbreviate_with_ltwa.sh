#!/usr/bin/env bash
set -euo pipefail

# Abbreviate BibTeX journal names according to LTWA using the local Python tool.
# Usage:
#   scripts/abbreviate_with_ltwa.sh references.bib [OUT] [REPORT]
# If OUT is omitted, writes to references.abbrev.bib. If REPORT is omitted, writes abbrev_report.txt.

IN=${1:-references.bib}
OUT=${2:-references.abbrev.bib}
REPORT=${3:-abbrev_report.txt}

HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$HERE/abbreviate_journals.py"

python "$PY" --bib "$IN" --out "$OUT" --report "$REPORT" --drop-stopwords
echo "Abbreviated journals written to: $OUT"
echo "Report: $REPORT"

