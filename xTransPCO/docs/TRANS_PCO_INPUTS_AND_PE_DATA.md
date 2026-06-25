# trans-PCO inputs and how PE multiomics data can be used

This note clarifies what original trans-PCO needs and how PE/placental multiomics datasets can be incorporated into the TANGO benchmark.

## 1. Inputs of a trans-PCO-style module-level QTL test

For one SNP and one module with K molecular features, a trans-PCO-style test needs:

```text
Z: K-dimensional SNP-feature association Z-score vector
R: K x K feature-feature correlation/covariance matrix
M: module definition, i.e. feature set membership
```

Optional inputs:

```text
G: biological network matrix, used by TANGO network component
A: annotation/prior information, such as PE relevance, placenta specificity, cis-QTL support
```

## 2. Individual-level version

A full individual-level pipeline needs:

```text
genotype matrix
expression/protein/methylation matrix
covariate matrix
module definitions
```

From these, one can compute:

```text
SNP-feature association Z scores
feature correlation matrix R
module PCs or other module summaries
```

This is the most complete benchmark setting, but it requires genotype plus molecular matrix from the same individuals.

## 3. Summary-statistics version

A summary-statistics pipeline needs:

```text
published SNP-feature Z-score table
module definitions
feature correlation matrix R
```

The feature correlation matrix can be estimated from:

1. null SNP Z-score correlations;
2. an external reference molecular matrix;
3. a shrinkage identity approximation as sensitivity analysis.

This is the correct setting for eQTLGen and UKB-PPP summary statistics.

## 4. Role of PE/placental multiomics data

Most PE/placental multiomics datasets do not include genotype for the same samples. Therefore they usually cannot directly provide QTL Z scores.

However, they are highly useful for TANGO in three ways:

### 4.1 Module construction

Use PE/placental multiomics matrices to define modules:

```text
placenta co-expression modules
condition-specific interomics communities
PE differential-expression gene sets
FGR/HDP/PE-specific subnetworks
miRNA-mRNA-protein-metabolite communities
```

These modules can then be tested using external QTL summary statistics.

### 4.2 Correlation matrix estimation

Use processed expression/protein/metabolite matrices to estimate within-module feature correlation R.

This gives a biologically matched placenta reference correlation matrix, even if QTL Z scores come from another dataset.

### 4.3 Disease relevance annotation

Use PE/placental multiomics results to score modules by disease relevance:

```text
PE differential signal
FGR + HDP specificity
placenta specificity
network centrality
known PE genes such as FLT1, FSTL3, HTRA4, LEP, miR-210-3p
```

## 5. The 2025 Communications Biology placental multiomics dataset

The article "Placental network differences among obstetric syndromes identified with an integrated multiomics approach" provides a very useful PE/placental multiomics resource.

Reported cohort:

```text
321 placentas
Control: 113
PTD: 71
PE: 71
FGR: 36
FGR + HDP: 30
```

Reported processed molecular layers:

```text
mRNA transcriptomics
miRNA transcriptomics
proteomics
metabolomics
placental histopathology
clinical data
condition-specific interomics communities
```

Best use in TANGO:

```text
module construction
placenta/PE reference correlation matrix
PE disease relevance annotation
network component input
```

Not sufficient by itself for QTL testing unless genotype data are available for the same samples.

## 6. Recommended benchmark design using PE data

A rigorous benchmark should separate QTL evidence from disease-module evidence.

### Step 1: Build PE/placenta modules

Use placental multiomics data to define modules and networks.

### Step 2: Obtain QTL Z scores

Use eQTLGen, GTEx, UKB-PPP, or another QTL summary-statistics dataset to obtain SNP-feature Z scores.

### Step 3: Match features

Intersect QTL features with PE module features.

### Step 4: Estimate R

Use one or more options:

```text
R_summary = correlation from null SNP Z scores
R_placenta = correlation from placental multiomics matrix
R_identity = identity matrix sensitivity control
```

### Step 5: Compare methods

Run all methods on the same SNP-module pairs:

```text
PC1
MinP
variance-component
original PCO or PCO-like implementation
TANGO
```

### Step 6: Evaluate

Compare:

```text
number of discoveries
calibration
replication across R choices
enrichment in PE/placenta modules
interpretability of top modules
runtime
```

## 7. Key wording for manuscript

Correct:

> PE/placental multiomics data were used to construct disease-relevant molecular modules and estimate placenta-specific module correlation structures. Independent public QTL summary statistics were then used to evaluate whether genetic variants exert trans-regulatory effects on these modules.

Incorrect:

> PE multiomics data alone were used to map trans-QTLs.

That is not valid unless the PE multiomics dataset also includes matched genotype data.
