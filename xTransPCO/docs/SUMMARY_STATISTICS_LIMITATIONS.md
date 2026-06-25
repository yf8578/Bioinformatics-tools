# Summary-statistics benchmark limitations

This document clarifies a key issue: eQTLGen and UKB-PPP primarily provide summary statistics, not the full individual-level molecular expression/protein matrices required to fully reproduce the original individual-level trans-PCO workflow.

## 1. What original individual-level trans-PCO needs

A full individual-level trans-PCO-style analysis needs:

1. genotype matrix;
2. molecular phenotype matrix, such as RNA expression or protein abundance;
3. covariates;
4. feature modules, for example WGCNA modules or curated pathways;
5. module-level feature correlation matrix;
6. SNP-feature association statistics.

The expression/protein matrix is needed for:

- constructing co-expression or co-abundance modules;
- estimating feature-feature correlation within each module;
- computing individual-level module PCs if using PC1 or PCO directly on molecular traits.

## 2. What eQTLGen provides

For public download, eQTLGen provides summary statistics, including SNP-gene Z scores, p-values, and sample-size related metadata. It does not provide the full individual-level expression matrix for all cohorts.

Therefore eQTLGen is suitable for:

- summary-statistics TANGO benchmark;
- summary-statistics PCO-like benchmark if a valid feature correlation matrix is estimated or supplied;
- testing whether module-level signals can be recovered from published SNP-gene association statistics.

It is not suitable for:

- full individual-level WGCNA reconstruction from the original cohort;
- exact reproduction of original individual-level trans-PCO preprocessing;
- exact individual-level module PC computation.

## 3. What UKB-PPP provides

UKB-PPP provides pQTL summary association resources through its portal. The public release is primarily suitable for summary-statistics pQTL analysis. Individual-level proteomics matrices are not generally treated as a simple open GitHub-downloadable file.

Therefore UKB-PPP is suitable for:

- protein-level summary-statistics TANGO benchmark;
- PPI or pathway module analysis using summary pQTL Z scores;
- testing whether network-smoothed components improve protein trans-QTL discovery.

It is not suitable for:

- direct full individual-level protein co-abundance module construction unless controlled-access individual-level data are available.

## 4. How to benchmark fairly without expression matrices

For summary-statistics benchmark, all methods should use the same input:

```text
SNP x feature Z-score matrix
module definitions
feature correlation matrix R
optional biological network matrix G
```

The feature correlation matrix can be obtained by:

1. estimating it from null SNP Z-score vectors in the same summary-statistics dataset;
2. using an external reference expression/protein matrix from a comparable tissue;
3. using a shrinkage identity approximation for sensitivity analysis;
4. using curated network modules and testing robustness across R choices.

## 5. Correct benchmark claims

Correct claim:

> TANGO can be benchmarked against PC1, MinP, variance-component, and summary-statistics PCO-like tests using public xQTL summary statistics.

Over-strong claim to avoid:

> eQTLGen or UKB-PPP alone allows exact reproduction of the original individual-level trans-PCO pipeline.

That is not true unless individual-level molecular matrices and genotype/covariate data are available.

## 6. Recommended benchmark tiers

Tier 1: simulation benchmark

- Full ground truth is known.
- Best for testing type I error and power.

Tier 2: summary-statistics benchmark

- Use eQTLGen, UKB-PPP, or other public summary statistics.
- Compare TANGO with summary-level PC1, MinP, variance-component, and PCO-like tests.

Tier 3: individual-level benchmark

- Use datasets with accessible genotype plus expression/protein matrix.
- This tier is needed for exact full-pipeline comparison with original trans-PCO.

Possible sources for Tier 3 include controlled-access cohorts or fully public model-organism systems genetics datasets.
