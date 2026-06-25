"""Command-line interface for TANGO.

Example
-------
tangoqtl run --z scores.tsv --module module.tsv --out result.tsv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .core import scan_modules, tango_test


def _read_modules(path: str) -> dict[str, list[str]]:
    """Read a two-column module file: module<TAB>feature."""

    df = pd.read_csv(path, sep="\t")
    required = {"module", "feature"}
    if not required.issubset(df.columns):
        raise ValueError("module file must contain columns: module, feature")
    out: dict[str, list[str]] = {}
    for module, sub in df.groupby("module"):
        out[str(module)] = sub["feature"].astype(str).tolist()
    return out


def run_one(args: argparse.Namespace) -> None:
    """Run TANGO for a single Z vector stored in a text file."""

    z = np.loadtxt(args.z)
    corr = np.loadtxt(args.corr) if args.corr else None
    network = np.loadtxt(args.network) if args.network else None
    res = tango_test(z, corr=corr, network=network)
    print(json.dumps(res.as_dict(), indent=2))


def run_scan(args: argparse.Namespace) -> None:
    """Run a module scan from a SNP-by-feature Z-score table."""

    z = pd.read_csv(args.z, sep="\t")
    modules = _read_modules(args.module)
    res = scan_modules(z, modules, snp_col=args.snp_col)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(args.out, sep="\t", index=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TANGO trans-QTL module tests")
    sub = parser.add_subparsers(dest="command", required=True)

    p_one = sub.add_parser("one", help="test one SNP-module Z vector")
    p_one.add_argument("--z", required=True, help="plain text file containing one Z vector")
    p_one.add_argument("--corr", default=None, help="optional correlation matrix text file")
    p_one.add_argument("--network", default=None, help="optional network matrix text file")
    p_one.set_defaults(func=run_one)

    p_scan = sub.add_parser("scan", help="scan SNP-by-feature Z table over modules")
    p_scan.add_argument("--z", required=True, help="TSV table: rows SNPs, columns features")
    p_scan.add_argument("--module", required=True, help="TSV file with columns module and feature")
    p_scan.add_argument("--snp-col", default="snp", help="column containing SNP ID")
    p_scan.add_argument("--out", required=True, help="output TSV path")
    p_scan.set_defaults(func=run_scan)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
