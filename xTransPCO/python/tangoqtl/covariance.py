"""Correlation and covariance utilities for TANGO.

Trans-QTL module tests are sensitive to the feature correlation matrix. In
individual-level data the matrix can be estimated from molecular phenotypes. In
summary-statistics data it can be estimated from null SNP Z-score vectors.
"""

from __future__ import annotations

import numpy as np


def _symmetrize(mat: np.ndarray) -> np.ndarray:
    """Force a matrix to be symmetric."""

    return (mat + mat.T) / 2.0


def shrink_correlation(corr: np.ndarray, shrinkage: float = 0.05, min_eigen: float = 1e-6) -> np.ndarray:
    """Regularize a feature correlation matrix.

    Parameters
    ----------
    corr:
        Square correlation matrix.
    shrinkage:
        Amount of shrinkage toward the identity matrix. A small value stabilizes
        near-singular module correlation matrices while keeping most biological
        correlation information.
    min_eigen:
        Minimum eigenvalue after projection. This prevents numerical failures in
        matrix inversion and quadratic forms.
    """

    c = np.asarray(corr, dtype=float)
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("corr must be a square matrix")
    if not (0.0 <= shrinkage <= 1.0):
        raise ValueError("shrinkage must be between 0 and 1")

    k = c.shape[0]
    c = _symmetrize(c)
    c = (1.0 - shrinkage) * c + shrinkage * np.eye(k)

    # Project to the positive semi-definite cone by clipping eigenvalues.
    vals, vecs = np.linalg.eigh(c)
    vals = np.clip(vals, min_eigen, None)
    c_psd = (vecs * vals) @ vecs.T
    c_psd = _symmetrize(c_psd)

    # Convert back to a correlation matrix with diagonal exactly one.
    d = np.sqrt(np.clip(np.diag(c_psd), min_eigen, None))
    c_cor = c_psd / np.outer(d, d)
    np.fill_diagonal(c_cor, 1.0)
    return _symmetrize(c_cor)


def estimate_null_correlation(null_z: np.ndarray, shrinkage: float = 0.05) -> np.ndarray:
    """Estimate feature correlation from null SNP Z-score vectors.

    Parameters
    ----------
    null_z:
        Matrix with shape ``n_null_snps x n_features``. Rows should be SNPs that
        are not expected to have true trans effects on the tested module.
    shrinkage:
        Shrinkage passed to :func:`shrink_correlation`.
    """

    z = np.asarray(null_z, dtype=float)
    if z.ndim != 2:
        raise ValueError("null_z must be a two-dimensional matrix")
    if z.shape[0] < 3:
        raise ValueError("at least three null SNPs are required to estimate correlation")

    c = np.corrcoef(z, rowvar=False)
    c = np.nan_to_num(c, nan=0.0, posinf=0.0, neginf=0.0)
    np.fill_diagonal(c, 1.0)
    return shrink_correlation(c, shrinkage=shrinkage)


def normalize_network(network: np.ndarray, add_identity: bool = True) -> np.ndarray:
    """Normalize a biological network matrix for network-smoothed testing.

    The input can be a binary adjacency matrix or a weighted graph. The output is
    a symmetric row/column-normalized matrix that is suitable for smoothing Z
    scores. This is intentionally conservative: it does not assume the graph is a
    perfect regulatory network.
    """

    w = np.asarray(network, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1]:
        raise ValueError("network must be a square matrix")
    w = np.maximum(_symmetrize(w), 0.0)
    if add_identity:
        w = w + np.eye(w.shape[0])
    deg = np.sum(w, axis=1)
    deg = np.where(deg <= 0, 1.0, deg)
    d_inv_sqrt = 1.0 / np.sqrt(deg)
    return (d_inv_sqrt[:, None] * w) * d_inv_sqrt[None, :]
