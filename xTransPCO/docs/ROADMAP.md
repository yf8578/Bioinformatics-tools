# TANGO development roadmap

This document lists the next development steps required to convert the current prototype into a publishable R/Python package and a dissertation method chapter.

## Phase 1: Minimal working method

Completed in the current prototype:

- Python implementation of dense, variance-component, sparse, and network-smoothed tests.
- ACAT omnibus combination.
- Correlation matrix shrinkage.
- Null-Z correlation estimation.
- Command-line interface.
- R implementation of the same core test.
- Method derivation document.

## Phase 2: Benchmarking

Required scripts:

1. Simulate null Z vectors and evaluate p-value calibration.
2. Simulate dense concordant effects.
3. Simulate sparse effects.
4. Simulate mixed-direction effects.
5. Simulate graph-localized effects.
6. Simulate near-singular module correlation matrices.

Competing methods:

- PC1 test.
- MinP test.
- Variance-component test.
- Original PCO if code is available.
- TANGO.

## Phase 3: Summary-statistics workflow

Required utilities:

- Read SNP-by-feature Z-score matrices.
- Read module files.
- Estimate module correlation matrices from null SNPs.
- Batch-scan SNP-module pairs.
- LD-clump significant SNP-module pairs.
- Export publication-ready result tables.

## Phase 4: Real public data applications

Suggested applications:

1. eQTLGen trans-eQTL module mapping.
2. GTEx tissue-specific module mapping.
3. UKB-PPP pQTL/PPI module mapping.
4. PE/placenta module application using public PE transcriptome and methylome modules.

## Phase 5: Manuscript and release

Required materials:

- Full mathematical derivation.
- Simulation benchmark figures.
- Real-data application figures.
- Python API documentation.
- R package vignette.
- GitHub Actions CI.
- Tagged release v0.1.0.
