# xTransPCO

`xTransPCO` is a research prototype for **adaptive, network-informed trans-QTL module mapping**. It treats trans-PCO as a general framework and focuses on improving the final multivariate module-level test.

The key idea is simple: original trans-PCO mainly uses PC-based omnibus testing, while trans-regulatory effects can follow several architectures. Some SNPs may weakly affect many genes in a module, some may strongly affect only a few genes, some may affect genes in opposite directions, and some effects may propagate along a biological network such as PPI, TF-target, pathway, or co-expression graph. `xTransPCO` combines tests for these effect patterns and returns a single module-level p-value.

## Repository layout

```text
xTransPCO/
├── pyproject.toml                 # Python package metadata
├── src/xtranspco/                 # Python implementation
│   ├── __init__.py
│   ├── core.py                    # Main adaptive omnibus test
│   ├── stats.py                   # Statistical utility functions
│   ├── covariance.py              # Correlation/covariance regularization
│   ├── simulation.py              # Simulation functions
│   └── cli.py                     # Command-line interface
├── examples/python_quickstart.py  # Minimal Python example
├── tests/test_core.py             # Python tests
└── rpkg/                          # R package implementation
    ├── DESCRIPTION
    ├── NAMESPACE
    ├── R/
    │   ├── adaptive_omnibus_test.R
    │   ├── stats.R
    │   ├── covariance.R
    │   └── simulation.R
    ├── examples/r_quickstart.R
    └── tests/testthat/
        ├── test_core.R
        └── testthat.R
```

## Inputs

For one SNP and one molecular module, the core input is:

- `z`: a numeric vector of length `K`; each element is the association Z score between the SNP and one molecular feature in the module.
- `corr`: a `K x K` feature correlation matrix. This can be estimated from individual-level molecular data or from null SNP Z-score vectors when only summary statistics are available.
- `network`: optional `K x K` biological network matrix. It can represent PPI adjacency, TF-target edges, pathway connectivity, or co-expression edges.

For genome-wide scans, repeat this test over many SNP-module pairs.

## Tests implemented

`xTransPCO` currently combines four complementary components:

1. **Dense burden test**: detects concordant weak effects across many module features.
2. **Variance-component test**: detects multi-feature effects with heterogeneous directions.
3. **Sparse MinP test**: detects a small subset of strongly affected features.
4. **Network-smoothed test**: detects signals coherent over a biological graph.

The component p-values are combined with ACAT/Cauchy combination.

## Python quick start

```bash
cd xTransPCO
python -m pip install -e .
python examples/python_quickstart.py
```

```python
import numpy as np
from xtranspco import adaptive_omnibus_test

z = np.array([2.1, 1.7, -0.4, 0.8, 1.2])
corr = np.eye(len(z))
result = adaptive_omnibus_test(z, corr=corr)
print(result)
```

## R quick start

```r
setwd("xTransPCO/rpkg")
# install.packages("devtools")
devtools::load_all(".")

z <- c(2.1, 1.7, -0.4, 0.8, 1.2)
corr <- diag(length(z))
adaptive_omnibus_test(z, corr = corr)
```

## Method positioning

Suggested method name:

> xTransPCO: an adaptive network-kernel omnibus framework for detecting trans-regulatory effects on molecular modules

Suggested dissertation claim:

> Instead of assuming that the first few expression PCs capture all trans-regulatory architectures, xTransPCO adaptively combines dense, sparse, variance-component, and network-coherent evidence to improve robustness across heterogeneous trans-QTL effect patterns.

## Status

This is an early research implementation with clear comments. Before formal package release, the next steps are benchmarking against original trans-PCO, PC1, MinP, and SKAT-like tests; adding real public xQTL data parsers; and adding long-form vignettes.

## License

MIT
