# Corrected dataset roles for TANGO/trans-PCO benchmark

This note corrects the earlier oversimplified statement about public datasets.
Some datasets do contain molecular matrices, and some datasets contain QTL results. The key is to classify them by what they can provide for a trans-PCO-style or TANGO benchmark.

## 1. Required inputs

For one SNP-module test:

```text
Z: SNP-feature association Z-score vector
R: feature-feature correlation matrix
M: module membership
G: optional network matrix
```

A dataset may provide all or only part of these inputs.

## 2. Placental multiomics dataset: Piekos et al. 2025

Repository:

```text
spiekos/Hood-Lab-Placental-Multiomics
```

The user's GitHub account also has an accessible copy:

```text
yf8578/Hood-Lab-Placental-Multiomics
```

This dataset provides processed multiomics matrices and networks:

```text
processed transcriptomic matrix
processed miRNA matrix
processed proteomic matrix
processed metabolomic matrix
placental histopathology reports
clinical data
raw, cleaned, and adjusted forms
cellular deconvolution results
condition-specific communities
analysis scripts
```

Best role in TANGO benchmark:

```text
module construction
feature correlation matrix R estimation
network/community matrix G construction
PE/placenta disease relevance annotation
```

This dataset is not primarily a QTL dataset unless matched genotype or QTL output is provided elsewhere.

## 3. Multiomics + QTL dataset: pluripotent proteome study

Paper:

```text
Genetic dissection of the pluripotent proteome through multi-omics data integration
```

This is a strong benchmark source because it contains multiomics data and genetic mapping results.

Reported data types:

```text
proteomics matrix for Diversity Outbred mESC lines
RNA-seq data
ATAC-seq data
genetic mapping results
pQTLs
eQTLs
caQTLs
QTL hotspots
MOFA factors
```

Data availability reported in the paper:

```text
ProteomeXchange / PRIDE: PXD033001
RNA-seq ArrayExpress: E-MTAB-7728
ATAC-seq ArrayExpress: E-MTAB-8759
processed data and code: Figshare DOI 10.6084/m9.figshare.22012850
```

Best role in TANGO benchmark:

```text
individual-level-like matrix benchmark if processed matrices are available
summary QTL benchmark using reported QTL scans
multiomics benchmark for pQTL/eQTL/caQTL modules
hotspot-based benchmark for trans effects
```

This dataset is not PE-specific, but it is methodologically valuable because it has both molecular matrices and QTL results.

## 4. eQTLGen and UKB-PPP

eQTLGen and UKB-PPP are still useful, but mainly as large-scale summary-statistics benchmarks.

They provide:

```text
large SNP-feature association summary statistics
large sample size
external replication and scaling benchmark
```

They usually do not provide simple open individual-level expression/protein matrices.

## 5. Recommended benchmark hierarchy

### Tier A: Matrix plus QTL benchmark

Use datasets with both molecular matrices and QTL results. This is the best setting for comparing TANGO with trans-PCO because R can be estimated directly from molecular matrices.

Candidate:

```text
Aydin et al. 2023 pluripotent proteome multiomics QTL dataset
```

### Tier B: PE/placenta disease module benchmark

Use PE multiomics matrices to define disease modules and estimate placenta-specific R.

Candidate:

```text
Piekos et al. 2025 Hood-Lab-Placental-Multiomics
```

Then combine these modules with external QTL Z scores.

### Tier C: Large public summary-statistics benchmark

Use eQTLGen, GTEx, UKB-PPP, GoDMC, or other public xQTL summary statistics.

## 6. Correct statement

The strongest design is:

```text
Use matrix-plus-QTL datasets for method benchmark against trans-PCO, and use PE/placental multiomics datasets for disease-relevant module construction and placenta-specific correlation estimation.
```

This avoids confusing PE module data with QTL data while still using all previously identified datasets productively.
