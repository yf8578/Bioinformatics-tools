#!/usr/bin/env bash
set -euo pipefail

# Download public benchmark resources for TANGO.
# Large raw files are intentionally downloaded into data/raw/, which should be
# ignored by git. Do not commit large xQTL summary-statistics files to GitHub.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DIR="${ROOT_DIR}/data/raw"

mkdir -p "${RAW_DIR}/eqtlgen/trans" "${RAW_DIR}/eqtlgen/cis"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "ERROR: command not found: $1" >&2
    exit 1
  }
}

need_cmd wget

# eQTLGen trans-eQTL summary statistics.
wget -c \
  -O "${RAW_DIR}/eqtlgen/trans/2018-09-04-trans-eQTLsFDR-CohortInfoRemoved-BonferroniAdded.txt.gz" \
  "https://download.gcc.rug.nl/downloads/eqtlgen/trans-eqtl/2018-09-04-trans-eQTLsFDR-CohortInfoRemoved-BonferroniAdded.txt.gz"

wget -c \
  -O "${RAW_DIR}/eqtlgen/trans/README_trans" \
  "https://download.gcc.rug.nl/downloads/eqtlgen/trans-eqtl/README_trans"

# eQTLGen cis-eQTL summary statistics for mediator annotation.
wget -c \
  -O "${RAW_DIR}/eqtlgen/cis/2019-12-11-cis-eQTLsFDR-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz" \
  "https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/2019-12-11-cis-eQTLsFDR-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz"

wget -c \
  -O "${RAW_DIR}/eqtlgen/cis/README_cis" \
  "https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/README_cis"

cat <<'EOF'

Download complete for direct eQTLGen files.

For GTEx v8, UKB-PPP, GoDMC, STRING, Reactome, and MSigDB, use the official portals listed in:
  data/DATASETS.md
  data/public_xqtl_manifest.tsv

EOF
