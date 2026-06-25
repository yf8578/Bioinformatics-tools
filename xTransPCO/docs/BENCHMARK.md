# Benchmark design: TANGO vs trans-PCO

This document defines the benchmark plan for comparing TANGO with original trans-PCO and simpler module tests.

## 1. Methods to compare

Minimum competitors:

1. PC1 test: association with the first module principal component.
2. MinP: minimum feature-level p-value with effective-test correction.
3. Variance-component test: quadratic Z-score test.
4. Original PCO: the original PC-based omnibus test if code is available.
5. TANGO: dense + variance-component + sparse + optional network component.

## 2. Simulation benchmark

Simulation should be used first because the ground truth is known.

Scenarios:

1. Null: no affected features.
2. Dense concordant: many affected features with same effect direction.
3. Dense mixed: many affected features with mixed directions.
4. Sparse: only one or a few affected features.
5. Network-localized: affected features form a connected graph neighborhood.
6. Near-singular correlation: high feature correlation within large modules.

Metrics:

- empirical type I error;
- power at fixed alpha;
- p-value calibration;
- runtime;
- robustness to correlation estimation error.

## 3. Real-data benchmark: eQTLGen

Primary public benchmark:

```text
eQTLGen trans-eQTL summary statistics
```

Reason:

- It is expression-level trans-QTL data.
- It provides SNP-gene Z scores.
- It is directly relevant to the original trans-PCO setting.

Workflow:

```text
1. Download eQTLGen trans-eQTL file.
2. Convert long SNP-gene table into SNP x gene Z-score matrix.
3. Define modules from WGCNA, GO, Reactome, or selected benchmark modules.
4. Estimate module correlation matrices from null SNP Z-score vectors.
5. Run all competing methods on the same SNP-module pairs.
6. Compare discoveries, calibration, replication, and biological enrichment.
```

## 4. Real-data benchmark: UKB-PPP pQTL

Secondary benchmark:

```text
UKB-PPP pQTL summary statistics
```

Reason:

- TANGO has a network-smoothed component.
- Protein-level trans effects are expected to be enriched in PPI and pathway relationships.

Workflow:

```text
1. Download summary statistics from UKB-PPP portal.
2. Map proteins to encoding genes and protein identifiers.
3. Construct PPI or Reactome modules.
4. Run TANGO with and without network component.
5. Test whether the network component improves discovery and interpretability.
```

## 5. Real-data benchmark: mQTL

Optional benchmark:

```text
GoDMC or eGTEx mQTL summary statistics
```

Purpose:

- Demonstrate that TANGO is not limited to expression or protein QTLs.
- Evaluate whether the same module-level test can work for methylation features.

## 6. Fairness rules

All methods must use:

- the same SNP-module pairs;
- the same feature set per module;
- the same feature correlation matrix;
- the same LD clumping procedure;
- the same FDR procedure.

## 7. Expected output tables

Recommended result schema:

```text
snp
module
method
pvalue
qvalue
n_features
component_pvalues
lead_feature
lead_feature_z
module_annotation
```

## 8. Recommended first reproducible benchmark

Start with a small eQTLGen subset:

```bash
bash scripts/download_public_data.sh
python scripts/prepare_eqtlgen_benchmark.py \
  --input data/raw/eqtlgen/trans/2018-09-04-trans-eQTLsFDR-CohortInfoRemoved-BonferroniAdded.txt.gz \
  --outdir data/interim/eqtlgen_small \
  --max-snps 2000 \
  --max-genes 500
```

Then run:

```bash
tangoqtl scan \
  --z data/interim/eqtlgen_small/eqtlgen_z_matrix.tsv \
  --module data/interim/eqtlgen_small/eqtlgen_modules.tsv \
  --out data/processed/eqtlgen_small/tango_results.tsv
```
