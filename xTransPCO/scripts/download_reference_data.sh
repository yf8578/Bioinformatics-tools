#!/usr/bin/env bash
set -euo pipefail

# This script records download entry points for benchmark data.
# It intentionally does not push downloaded files to GitHub.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DIR="${ROOT_DIR}/data/raw"
mkdir -p "${RAW_DIR}"

cat <<'EOF'
TANGO benchmark data sources
============================

1. PE/placenta matrix reference
   Repository: https://github.com/spiekos/Hood-Lab-Placental-Multiomics
   User copy:  https://github.com/yf8578/Hood-Lab-Placental-Multiomics

   Recommended use:
   - copy processed matrices from data/normalized_cleaned_adjusted/ or data/normalized_cleaned/
   - run scripts/prepare_matrix_reference.py to estimate module correlation matrices

2. Matrix + QTL method benchmark
   Aydin et al. 2023 pluripotent proteome multiomics QTL dataset
   - PRIDE / ProteomeXchange: PXD033001
   - RNA-seq ArrayExpress: E-MTAB-7728
   - ATAC-seq ArrayExpress: E-MTAB-8759
   - processed data and code: https://doi.org/10.6084/m9.figshare.22012850

3. Large summary-statistics benchmark
   eQTLGen trans-eQTL: https://www.eqtlgen.org/trans-eqtls.html
   eQTLGen cis-eQTL:   https://www.eqtlgen.org/cis-eqtls.html
   UKB-PPP pQTL:       http://ukb-ppp.gwas.eu
   GTEx v8 QTL:        https://gtexportal.org/home/downloads/adult-gtex/qtl

Do not commit large raw files. Put them under data/raw/, data/interim/, or data/processed/.
EOF
