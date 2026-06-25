#!/usr/bin/env python3
"""Prepare eQTLGen trans-eQTL data for TANGO/trans-PCO benchmarking.

The eQTLGen trans-eQTL file is a long table with SNP-gene association records.
For module-level tests, we need a SNP-by-gene Z-score matrix and a module file.

This script builds a small or medium benchmark matrix by selecting the most
frequently tested/observed genes and SNPs from the long table. For full-scale
benchmarking, adapt the selection criteria to your target modules.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def guess_col(columns: list[str], candidates: list[str]) -> str:
    """Return the first matching column name from a list of candidates."""

    lower_map = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    raise ValueError(f"Cannot find any of these columns: {candidates}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare eQTLGen benchmark input files")
    parser.add_argument("--input", required=True, help="eQTLGen trans-eQTL txt.gz file")
    parser.add_argument("--outdir", required=True, help="output directory")
    parser.add_argument("--max-snps", type=int, default=2000, help="maximum SNPs to retain")
    parser.add_argument("--max-genes", type=int, default=500, help="maximum genes to retain")
    parser.add_argument("--sep", default="\t", help="input separator")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("Reading eQTLGen table...")
    df = pd.read_csv(args.input, sep=args.sep, compression="infer")
    cols = list(df.columns)

    snp_col = guess_col(cols, ["SNP", "SNPName", "rsid", "variant"])
    gene_col = guess_col(cols, ["Gene", "GeneSymbol", "Probe", "gene"])
    z_col = guess_col(cols, ["Z-score", "Zscore", "Z", "z"])

    print(f"Detected columns: SNP={snp_col}, gene={gene_col}, z={z_col}")

    df = df[[snp_col, gene_col, z_col]].dropna()
    df.columns = ["snp", "gene", "z"]
    df["snp"] = df["snp"].astype(str)
    df["gene"] = df["gene"].astype(str)
    df["z"] = pd.to_numeric(df["z"], errors="coerce")
    df = df.dropna(subset=["z"])

    top_snps = df["snp"].value_counts().head(args.max_snps).index
    top_genes = df["gene"].value_counts().head(args.max_genes).index
    df = df[df["snp"].isin(top_snps) & df["gene"].isin(top_genes)]

    print("Pivoting to SNP x gene matrix...")
    mat = df.pivot_table(index="snp", columns="gene", values="z", aggfunc="first")
    mat = mat.fillna(0.0)
    mat.insert(0, "snp", mat.index)
    mat.to_csv(outdir / "eqtlgen_z_matrix.tsv", sep="\t", index=False)

    # A simple placeholder module file: all selected genes in one module.
    # Replace this with WGCNA, Reactome, GO, PPI, or PE-specific modules later.
    module = pd.DataFrame({"module": "eqtlgen_selected_genes", "feature": list(mat.columns[1:])})
    module.to_csv(outdir / "eqtlgen_modules.tsv", sep="\t", index=False)

    print("Done.")
    print(f"Z matrix: {outdir / 'eqtlgen_z_matrix.tsv'}")
    print(f"Module file: {outdir / 'eqtlgen_modules.tsv'}")


if __name__ == "__main__":
    main()
