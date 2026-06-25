#!/usr/bin/env python3
"""Prepare molecular matrix references for module-level QTL tests.

This script is intentionally generic. It can be used with PE/placenta matrices
from Piekos et al. or with any other expression/protein/metabolite matrix.

Input matrix formats supported:

1. samples x features, with a sample ID column;
2. features x samples, with a feature ID column.

The script outputs:

- a cleaned sample x feature matrix;
- a feature correlation matrix;
- a simple module file if no external module file is provided.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def read_matrix(path, sep, id_col, transpose):
    df = pd.read_csv(path, sep=sep)
    if id_col not in df.columns:
        raise ValueError(f"id column {id_col} not found")
    df = df.set_index(id_col)
    if transpose:
        df = df.T
    df = df.apply(pd.to_numeric, errors="coerce")
    return df


def filter_matrix(df, max_missing, min_sd):
    missing = df.isna().mean(axis=0)
    keep = missing <= max_missing
    df = df.loc[:, keep]
    df = df.fillna(df.median(axis=0))
    sd = df.std(axis=0)
    df = df.loc[:, sd >= min_sd]
    return df


def make_correlation(df, shrinkage):
    corr = df.corr().fillna(0.0)
    arr = corr.to_numpy(dtype=float)
    k = arr.shape[0]
    arr = (1 - shrinkage) * arr + shrinkage * np.eye(k)
    corr = pd.DataFrame(arr, index=corr.index, columns=corr.columns)
    return corr


def main():
    parser = argparse.ArgumentParser(description="Prepare matrix-derived reference correlation")
    parser.add_argument("--matrix", required=True, help="input molecular matrix")
    parser.add_argument("--outdir", required=True, help="output directory")
    parser.add_argument("--sep", default=",", help="input separator; use '\\t' for TSV")
    parser.add_argument("--id-col", required=True, help="sample or feature ID column")
    parser.add_argument("--transpose", action="store_true", help="input is features x samples")
    parser.add_argument("--module-name", default="matrix_reference_module")
    parser.add_argument("--max-missing", type=float, default=0.2)
    parser.add_argument("--min-sd", type=float, default=1e-8)
    parser.add_argument("--shrinkage", type=float, default=0.05)
    args = parser.parse_args()

    sep = "\t" if args.sep == "\\t" else args.sep
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = read_matrix(args.matrix, sep=sep, id_col=args.id_col, transpose=args.transpose)
    df = filter_matrix(df, max_missing=args.max_missing, min_sd=args.min_sd)
    corr = make_correlation(df, shrinkage=args.shrinkage)

    clean_path = outdir / "matrix_clean_samples_by_features.tsv"
    corr_path = outdir / "feature_correlation.tsv"
    module_path = outdir / "modules.tsv"

    df.to_csv(clean_path, sep="\t")
    corr.to_csv(corr_path, sep="\t")
    pd.DataFrame({"module": args.module_name, "feature": list(df.columns)}).to_csv(module_path, sep="\t", index=False)

    print(f"Clean matrix: {clean_path}")
    print(f"Correlation:  {corr_path}")
    print(f"Modules:      {module_path}")


if __name__ == "__main__":
    main()
