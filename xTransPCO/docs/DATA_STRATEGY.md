# Data strategy for TANGO benchmark

This document defines the clean benchmark strategy after separating three different data roles:

1. molecular matrix data;
2. QTL association data;
3. disease-specific module and network data.

## 1. What TANGO/trans-PCO-style tests require

For a single SNP-module test, the statistical input is:

```text
Z = SNP-feature association Z-score vector
R = feature-feature correlation matrix
M = feature module definition
G = optional biological network matrix
```

A dataset can provide all or only part of these inputs. The benchmark should not confuse these roles.

## 2. Matrix plus QTL datasets are best for method benchmark

The best benchmark dataset contains both molecular matrices and QTL results. This allows the same dataset to provide both:

```text
R from molecular matrix
Z from QTL mapping or reported QTL statistics
```

The current strongest candidate is:

```text
Aydin et al. 2023, Genetic dissection of the pluripotent proteome through multi-omics data integration
```

This dataset is not PE-specific, but it is methodologically valuable because it contains multiomics matrices and genetic mapping results. It should be used for the primary method benchmark against original trans-PCO-style tests.

## 3. PE/placenta multiomics datasets are disease-module references

The Piekos et al. 2025 placenta multiomics dataset provides processed transcriptomic, miRNA, proteomic, metabolomic, clinical, histopathology, and condition-specific community data. It is ideal for:

```text
PE/FGR/HDP module construction
placenta-specific R estimation
network/community definition
PE disease relevance annotation
```

It should not be treated as a QTL dataset unless matched genotype or QTL results are identified.

## 4. Large summary-statistics datasets are scale benchmarks

eQTLGen, UKB-PPP, GTEx, and similar resources are useful for large summary-statistics benchmarks. They are not the first choice for exact individual-level trans-PCO reproduction because the individual molecular matrices are usually not available as simple public files.

Use them for:

```text
large-scale SNP-feature Z-score input
external QTL evidence
replication and scaling tests
```

## 5. Recommended benchmark order

### Stage A: simulation

Use generated Z-score matrices with known effect architecture:

```text
null
dense concordant
sparse
mixed-direction
network-localized
near-singular correlation
```

This is the cleanest way to test type I error and power.

### Stage B: matrix plus QTL benchmark

Use Aydin et al. style multiomics QTL data. This is the best stage for comparing TANGO with original or PCO-like methods because both molecular matrices and QTL information are available.

### Stage C: PE/placenta application

Use Piekos et al. placenta multiomics data to build disease modules and reference correlations. Combine these modules with external QTL Z scores.

### Stage D: large summary-statistics benchmark

Use eQTLGen, UKB-PPP, GTEx, and other summary resources to show scalability.

## 6. Repository policy

Do not commit large raw datasets. Commit only:

```text
small manifest files
scripts
small simulated benchmark output
documentation
```

Raw data should be downloaded to:

```text
data/raw/
data/interim/
data/processed/
```

These paths are git-ignored.
