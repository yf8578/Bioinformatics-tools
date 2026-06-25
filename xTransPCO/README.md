# TANGO

TANGO means **Trans-regulatory Adaptive Network Gene-set Omnibus**.

This project started from the idea of improving trans-PCO. The method implemented here should not still be called PCO, because PCO means principal-component omnibus. TANGO is different: it combines dense, sparse, variance-component, and optional network-smoothed evidence for module-level trans-QTL testing.

## Core idea

A trans-PCO-style workflow has three parts:

1. prepare SNP-feature association statistics;
2. group molecular features into modules;
3. test each SNP-module pair.

TANGO improves the third part. It is a replacement or complement for the original PC-based omnibus test.

## Input

For one SNP and one module:

- `z`: vector of SNP-feature Z scores;
- `corr`: feature correlation matrix;
- `network`: optional biological graph matrix.

The features can be genes, proteins, CpG sites, metabolites, or other molecular traits.

## Implemented tests

TANGO currently combines:

1. dense burden test;
2. variance-component test;
3. sparse MinP test;
4. optional network-smoothed test.

The final p-value is computed by ACAT.

## Python quick start

```bash
cd xTransPCO
python -m pip install -e .
python examples/python_quickstart.py
```

```python
import numpy as np
from tangoqtl import tango_test

z = np.array([2.1, 1.7, -0.4, 0.8, 1.2])
corr = np.eye(len(z))
res = tango_test(z, corr=corr)
print(res.as_dict())
```

## R quick start

```r
setwd("xTransPCO/rpkg")
devtools::load_all(".")

z <- c(2.1, 1.7, -0.4, 0.8, 1.2)
corr <- diag(length(z))
tango_test(z, corr = corr)
```

## Directory layout

```text
xTransPCO/
├── pyproject.toml
├── python/tangoqtl/
├── rpkg/
├── docs/
├── examples/
└── tests/
```

## Method documents

- `docs/METHOD.md`: mathematical derivation.
- `docs/ROADMAP.md`: development roadmap.

## Dissertation positioning

TANGO generalizes the final module-level test of the trans-PCO framework from PC-space adaptivity to effect-architecture adaptivity. It targets dense, sparse, mixed-direction, and network-coherent trans-regulatory architectures.
