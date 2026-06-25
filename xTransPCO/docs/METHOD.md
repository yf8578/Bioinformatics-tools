# TANGO method derivation

TANGO means **Trans-regulatory Adaptive Network Gene-set Omnibus**. The name is intentionally different from PCO. PCO is a principal-component omnibus test; TANGO is an adaptive omnibus framework that combines multiple biological and statistical effect architectures.

## 1. Problem definition

For one SNP `s` and one molecular module `M` containing `K` features, let

```text
Z_sM = (Z_1, Z_2, ..., Z_K)^T
```

where `Z_j` is the marginal association Z score between SNP `s` and feature `j` in the module. The feature can be a gene, protein, CpG site, metabolite, splicing event, or any molecular trait with summary-level association statistics.

Under the null hypothesis,

```text
H0: SNP s has no trans-regulatory effect on any feature in module M.
```

The working null distribution is

```text
Z_sM ~ N(0, R_M),
```

where `R_M` is the within-module feature correlation matrix.

The alternative is broad:

```text
H1: SNP s affects at least one feature or one coherent substructure of module M.
```

The core difficulty is that trans-regulatory effects can be dense, sparse, mixed-direction, or coherent over a biological network.

## 2. Why not keep calling it PCO?

Original trans-PCO uses PC-based omnibus testing. It projects module-level Z scores onto principal components of the feature correlation matrix and combines several PC-based statistics. That is useful, but the innovation here is different.

TANGO does not assume that the optimal signal is captured by principal components. Instead, it explicitly builds component tests for different effect architectures:

1. concordant dense effects;
2. heterogeneous dense effects;
3. sparse effects;
4. network-coherent effects.

Therefore, the method should not be named PCO. It is a new adaptive omnibus test that can be inserted into the trans-PCO framework as a replacement for the final module-level test.

## 3. Input data

For one SNP-module pair, the minimal input is:

```text
z:      K-dimensional vector of association Z scores
R:      K x K feature correlation matrix
G:      optional K x K biological network matrix
```

For genome-wide scans, the input becomes a SNP-by-feature Z-score matrix plus a list of modules.

## 4. Dense burden component

The dense burden component targets concordant weak effects across many features.

Let

```text
w = (1, 1, ..., 1)^T.
```

The burden statistic is

```text
T_dense = (w^T Z)^2 / (w^T R w).
```

Under the null,

```text
T_dense ~ chi-square_1.
```

This component is powerful when many module features have weak effects in the same direction.

## 5. Variance-component component

The variance-component component targets dense effects with heterogeneous directions.

Use the quadratic statistic

```text
Q = Z^T Z.
```

If

```text
Z ~ N(0, R),
```

then

```text
Q = sum_i lambda_i * chi-square_i,
```

where `lambda_i` are eigenvalues of `R`. The exact mixture distribution can be computed by numerical methods such as Davies or Liu approximation. For the first implementation, TANGO uses a Satterthwaite approximation.

Match the first two moments:

```text
E(Q) = sum_i lambda_i
Var(Q) = 2 * sum_i lambda_i^2.
```

Approximate

```text
Q ~ a * chi-square_df,
```

where

```text
df = 2 * E(Q)^2 / Var(Q)
a  = Var(Q) / (2 * E(Q)).
```

This component is useful when positive and negative effects cancel in a burden test.

## 6. Sparse MinP component

The sparse component targets cases where only a few features in the module are affected.

For each feature,

```text
p_j = 2 * Phi(-abs(Z_j)).
```

The module-level sparse statistic is

```text
p_min = min_j p_j.
```

A simple effective-test Sidak correction is

```text
p_sparse = 1 - (1 - p_min)^m_eff.
```

The effective number of tests is estimated from eigenvalues of `R`:

```text
m_eff = sum_i min(lambda_i, 1).
```

This component is included because original PC-based tests may lose power when only one or a few module members are truly affected.

## 7. Network-smoothed component

If a biological network matrix `G` is available, TANGO tests whether effects are coherent over the graph.

First construct a normalized smoothing matrix:

```text
S = D^(-1/2) (G + I) D^(-1/2),
```

where `D` is the degree matrix of `G + I`.

Smooth the Z vector:

```text
Z_net = S Z.
```

The null covariance becomes

```text
R_net = S R S^T.
```

Then compute

```text
Q_net = Z_net^T Z_net.
```

Again use a Satterthwaite approximation based on eigenvalues of `R_net`.

This component is designed for PPI clusters, TF-target modules, pathway graphs, and disease-specific co-expression networks.

## 8. ACAT omnibus combination

Let the component p-values be

```text
p_1, p_2, ..., p_L.
```

TANGO combines them by ACAT:

```text
C = sum_l weight_l * tan[(0.5 - p_l) * pi]
```

and

```text
p_TANGO = 0.5 - arctan(C) / pi.
```

ACAT is useful because the component p-values are dependent: all of them are computed from the same module-level Z vector.

## 9. Relationship to original trans-PCO

Original trans-PCO:

```text
SNP -> module Z vector -> PC-based omnibus test
```

TANGO:

```text
SNP -> module Z vector -> adaptive architecture-aware omnibus test
```

Therefore, TANGO can be inserted into the original trans-PCO framework without changing the upstream data preprocessing or module construction steps.

## 10. Expected advantages

TANGO is expected to improve robustness in the following cases:

1. sparse trans effects, where only a few features in a module are affected;
2. mixed-direction effects, where burden tests cancel out;
3. network-localized effects, where affected features cluster in PPI or pathway space;
4. large modules with unstable principal components, where shrinkage improves correlation estimation.

## 11. Simulation plan

The recommended benchmark should compare:

- PC1 module test;
- MinP;
- original PCO;
- SKAT-like variance-component test;
- TANGO.

Simulated architectures:

1. null;
2. dense concordant weak effects;
3. dense mixed-direction weak effects;
4. sparse strong effects;
5. network-localized effects;
6. large-module near-singular correlation matrices.

Key evaluation metrics:

- type I error;
- statistical power;
- calibration of p-values;
- robustness to correlation matrix estimation error;
- runtime.

## 12. Practical data sources

The method can be applied to:

- eQTLGen trans-eQTL summary statistics;
- GTEx tissue-specific QTL summary statistics;
- GoDMC or eGTEx mQTL summary statistics;
- UKB-PPP pQTL summary statistics;
- PE or placenta-specific public transcriptome and methylome modules.

## 13. Dissertation-level statement

TANGO is not merely a reimplementation of trans-PCO. It generalizes the final module-level test from PC-space adaptivity to effect-architecture adaptivity, allowing trans-QTL module detection across dense, sparse, mixed, and network-coherent regulatory patterns.
