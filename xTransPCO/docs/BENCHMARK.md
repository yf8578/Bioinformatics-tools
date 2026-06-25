# Benchmark design: TANGO vs trans-PCO-style tests

This benchmark plan separates method validation from disease application.

## 1. Methods to compare

Implemented now:

```text
PC1
MinP
variance-component
PCO-like ACAT baseline
TANGO
```

Important note: `pco_acat` is a lightweight PC-based omnibus baseline. It is not an exact reproduction of the original six-test PCO implementation. If original trans-PCO code is obtained, it should be added as an external method wrapper.

## 2. Stage A: simulation benchmark

This is the first benchmark and is already supported by:

```text
scripts/benchmark_simulation.py
```

Scenarios:

```text
null
dense concordant
sparse
mixed-direction
network-localized
```

Metrics:

```text
type I error under null
power under alternatives
p-value calibration
runtime
relative gain over PC1, MinP, VC, and PCO-like baseline
```

Run:

```bash
python scripts/benchmark_simulation.py \
  --out results/simulation_benchmark.tsv \
  --n-rep 200 \
  --k 50 \
  --effect 0.6 \
  --prop 0.1
```

## 3. Stage B: matrix plus QTL benchmark

This is the best real-data method benchmark because both `R` and `Z` can be obtained from matched or linked resources.

Primary candidate:

```text
Aydin et al. 2023 pluripotent proteome multiomics QTL dataset
```

Use:

```text
molecular matrices -> estimate R
reported QTL results or re-mapped QTL -> construct Z
GO/pathway/factor/hotspot modules -> define M
```

This stage should be used to compare TANGO against original trans-PCO-style methods most fairly.

## 4. Stage C: PE/placenta matrix application

Primary PE dataset:

```text
Piekos et al. 2025 Hood-Lab-Placental-Multiomics
```

Use this dataset for:

```text
PE/FGR/HDP module construction
placenta-specific R estimation
condition-specific network/community G
PE disease relevance annotation
```

Then combine these modules with external QTL Z scores. This is an application layer, not necessarily a complete QTL benchmark by itself.

## 5. Stage D: large summary-statistics benchmark

Use:

```text
eQTLGen trans-eQTL
GTEx QTL
UKB-PPP pQTL
GoDMC/eGTEx mQTL if accessible
```

Use this stage for scale and external biological validation. Do not claim exact individual-level trans-PCO reproduction from summary-only resources.

## 6. Fairness rules

All methods must use the same:

```text
SNP-module pairs
feature set per module
feature correlation matrix R
LD pruning or clumping procedure
FDR procedure
```

## 7. Output schema

Recommended result table:

```text
dataset
stage
snp
module
method
pvalue
qvalue
n_features
n_causal_if_simulated
effect_architecture
runtime_seconds
notes
```
