"""Core TANGO tests.

TANGO stands for Trans-regulatory Adaptive Network Gene-set Omnibus.

The goal is to replace a purely PC-based module test with an adaptive test that
covers several plausible trans-regulatory architectures:

1. Dense concordant effects: many module features move in the same direction.
2. Dense heterogeneous effects: many features move, but directions can differ.
3. Sparse effects: only a small subset of features is affected.
4. Network-coherent effects: affected features cluster on a known biological graph.

The final p-value is obtained by ACAT combination of component p-values.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
from scipy import stats

from .covariance import normalize_network, shrink_correlation
from .stats import acat, li_ji_effective_tests, minp_sidak, two_sided_z_pvalue


@dataclass(frozen=True)
class TangoResult:
    """Result object returned by :func:`tango_test`.

    Attributes
    ----------
    pvalue:
        Final ACAT-combined omnibus p-value.
    dense_pvalue:
        Dense burden test p-value.
    vc_pvalue:
        Variance-component test p-value.
    sparse_pvalue:
        Sparse MinP test p-value.
    network_pvalue:
        Network-smoothed test p-value. ``None`` if no network was supplied.
    component_pvalues:
        Dictionary of component p-values used in ACAT.
    statistics:
        Dictionary of raw component statistics.
    n_features:
        Number of features in the tested module.
    """

    pvalue: float
    dense_pvalue: float
    vc_pvalue: float
    sparse_pvalue: float
    network_pvalue: float | None
    component_pvalues: Mapping[str, float]
    statistics: Mapping[str, float]
    n_features: int

    def as_dict(self) -> dict[str, float | int | None]:
        """Convert the result to a flat dictionary for data-frame output."""

        out: dict[str, float | int | None] = {
            "pvalue": self.pvalue,
            "dense_pvalue": self.dense_pvalue,
            "vc_pvalue": self.vc_pvalue,
            "sparse_pvalue": self.sparse_pvalue,
            "network_pvalue": self.network_pvalue,
            "n_features": self.n_features,
        }
        for key, value in self.statistics.items():
            out[f"stat_{key}"] = value
        return out


def _validate_inputs(z: Sequence[float], corr: np.ndarray | None) -> tuple[np.ndarray, np.ndarray]:
    """Validate and regularize a Z vector and correlation matrix."""

    z_arr = np.asarray(z, dtype=float)
    if z_arr.ndim != 1:
        raise ValueError("z must be a one-dimensional vector")
    if z_arr.size < 2:
        raise ValueError("at least two module features are required")
    if not np.all(np.isfinite(z_arr)):
        raise ValueError("z contains non-finite values")

    if corr is None:
        c = np.eye(z_arr.size)
    else:
        c = np.asarray(corr, dtype=float)
        if c.shape != (z_arr.size, z_arr.size):
            raise ValueError("corr must have shape len(z) x len(z)")
    c = shrink_correlation(c)
    return z_arr, c


def dense_burden_test(z: np.ndarray, corr: np.ndarray) -> tuple[float, float]:
    """Dense concordant-effect burden test.

    Statistic:
        T = (1'Z)^2 / (1'R1)

    Under the null, T approximately follows chi-square with 1 degree of freedom.
    This component is powerful when many features show weak effects in the same
    direction.
    """

    w = np.ones(z.size)
    denom = float(w @ corr @ w)
    denom = max(denom, 1e-12)
    stat = float((w @ z) ** 2 / denom)
    p = float(stats.chi2.sf(stat, df=1))
    return stat, p


def variance_component_test(z: np.ndarray, corr: np.ndarray) -> tuple[float, float]:
    """Dense heterogeneous-direction variance-component test.

    We use the quadratic statistic Q = Z'Z. If Z ~ N(0, R), Q follows a mixture
    of chi-square distributions with weights equal to eigenvalues of R. For a
    lightweight first implementation, we use a Satterthwaite approximation:

        Q ~ scale * chi-square(df)

    where df and scale match the first two moments of Q.
    """

    eig = np.linalg.eigvalsh(corr)
    eig = np.clip(eig, 0.0, None)
    mean_q = float(np.sum(eig))
    var_q = float(2.0 * np.sum(eig**2))
    if var_q <= 0 or mean_q <= 0:
        raise ValueError("invalid correlation eigenvalues")
    df = 2.0 * mean_q**2 / var_q
    scale = var_q / (2.0 * mean_q)
    stat = float(z @ z)
    p = float(stats.chi2.sf(stat / scale, df=df))
    return stat, p


def sparse_minp_test(z: np.ndarray, corr: np.ndarray) -> tuple[float, float]:
    """Sparse-effect MinP test with effective-test correction."""

    feature_p = two_sided_z_pvalue(z)
    meff = li_ji_effective_tests(corr)
    p = minp_sidak(feature_p, effective_tests=meff)
    stat = float(np.max(np.abs(z)))
    return stat, p


def network_smoothed_test(z: np.ndarray, corr: np.ndarray, network: np.ndarray) -> tuple[float, float]:
    """Network-coherent signal test.

    The network matrix is normalized to S. We smooth the Z vector as S Z and test
    the quadratic statistic in the smoothed space. The null covariance is S R S'.
    A Satterthwaite approximation is again used for the quadratic form.
    """

    s = normalize_network(network)
    if s.shape != corr.shape:
        raise ValueError("network must have the same shape as corr")
    z_smooth = s @ z
    cov_smooth = s @ corr @ s.T
    cov_smooth = shrink_correlation(cov_smooth)

    eig = np.linalg.eigvalsh(cov_smooth)
    eig = np.clip(eig, 0.0, None)
    mean_q = float(np.sum(eig))
    var_q = float(2.0 * np.sum(eig**2))
    df = 2.0 * mean_q**2 / var_q
    scale = var_q / (2.0 * mean_q)
    stat = float(z_smooth @ z_smooth)
    p = float(stats.chi2.sf(stat / scale, df=df))
    return stat, p


def tango_test(
    z: Sequence[float],
    corr: np.ndarray | None = None,
    network: np.ndarray | None = None,
    component_weights: Mapping[str, float] | None = None,
) -> TangoResult:
    """Run the TANGO adaptive omnibus test for one SNP-module pair.

    Parameters
    ----------
    z:
        Vector of SNP-feature association Z scores for one module.
    corr:
        Feature correlation matrix. If omitted, an identity matrix is used. For
        real xQTL scans, users should provide a matrix estimated from individual
        molecular data or null SNP summary statistics.
    network:
        Optional biological network matrix. If supplied, a network-smoothed test
        is included in the omnibus combination.
    component_weights:
        Optional ACAT weights for component tests. Keys can be ``dense``, ``vc``,
        ``sparse``, and ``network``.

    Returns
    -------
    TangoResult
        Component p-values, statistics, and final omnibus p-value.
    """

    z_arr, c = _validate_inputs(z, corr)

    dense_stat, dense_p = dense_burden_test(z_arr, c)
    vc_stat, vc_p = variance_component_test(z_arr, c)
    sparse_stat, sparse_p = sparse_minp_test(z_arr, c)

    component_p = {
        "dense": dense_p,
        "vc": vc_p,
        "sparse": sparse_p,
    }
    stats_dict = {
        "dense": dense_stat,
        "vc": vc_stat,
        "sparse": sparse_stat,
    }
    network_p: float | None = None

    if network is not None:
        net_stat, network_p = network_smoothed_test(z_arr, c, np.asarray(network, dtype=float))
        component_p["network"] = network_p
        stats_dict["network"] = net_stat

    if component_weights is None:
        weights = None
    else:
        weights = [component_weights.get(name, 0.0) for name in component_p]

    final_p = acat(list(component_p.values()), weights=weights)

    return TangoResult(
        pvalue=final_p,
        dense_pvalue=dense_p,
        vc_pvalue=vc_p,
        sparse_pvalue=sparse_p,
        network_pvalue=network_p,
        component_pvalues=component_p,
        statistics=stats_dict,
        n_features=z_arr.size,
    )


def scan_modules(
    z_matrix: pd.DataFrame,
    modules: Mapping[str, Sequence[str]],
    corr_matrices: Mapping[str, np.ndarray] | None = None,
    networks: Mapping[str, np.ndarray] | None = None,
    snp_col: str | None = None,
) -> pd.DataFrame:
    """Scan many SNPs across many modules.

    Parameters
    ----------
    z_matrix:
        Data frame whose rows are SNPs and columns are molecular features. Values
        are association Z scores. If ``snp_col`` is supplied, that column is used
        as SNP identifier and removed from the feature matrix.
    modules:
        Mapping from module name to feature names.
    corr_matrices:
        Optional mapping from module name to module-specific correlation matrix.
    networks:
        Optional mapping from module name to module-specific network matrix.
    snp_col:
        Optional column containing SNP IDs.

    Returns
    -------
    pandas.DataFrame
        One row per SNP-module pair.
    """

    if snp_col is not None:
        snp_ids = z_matrix[snp_col].astype(str).to_numpy()
        z_df = z_matrix.drop(columns=[snp_col])
    else:
        snp_ids = z_matrix.index.astype(str).to_numpy()
        z_df = z_matrix

    rows: list[dict[str, float | int | str | None]] = []
    for module_name, features in modules.items():
        feature_list = [f for f in features if f in z_df.columns]
        if len(feature_list) < 2:
            continue
        corr = None if corr_matrices is None else corr_matrices.get(module_name)
        network = None if networks is None else networks.get(module_name)

        for idx, snp in enumerate(snp_ids):
            z = z_df.iloc[idx][feature_list].to_numpy(dtype=float)
            res = tango_test(z, corr=corr, network=network)
            item = res.as_dict()
            item["snp"] = snp
            item["module"] = module_name
            rows.append(item)

    return pd.DataFrame(rows)
