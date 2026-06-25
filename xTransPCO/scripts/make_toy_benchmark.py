#!/usr/bin/env python3
"""Generate tiny benchmark data that can be committed to GitHub.

This toy dataset is not for scientific conclusions. It exists to make sure that
TANGO, PC1, MinP, and future trans-PCO wrappers all receive the same input
format.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Create toy SNP-by-feature benchmark data")
    parser.add_argument("--outdir", default="data/toy", help="output directory")
    parser.add_argument("--n-snps", type=int, default=20)
    parser.add_argument("--n-features", type=int, default=12)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    snps = [f"rs{i+1}" for i in range(args.n_snps)]
    features = [f"GENE{i+1}" for i in range(args.n_features)]

    z = rng.normal(size=(args.n_snps, args.n_features))

    # Add two simple positive-control signals.
    z[0, 0:5] += 2.0      # dense block
    z[1, 9] += 4.0        # sparse signal

    z_df = pd.DataFrame(z, columns=features)
    z_df.insert(0, "snp", snps)
    z_df.to_csv(outdir / "toy_z_matrix.tsv", sep="\t", index=False)

    modules = []
    for f in features[:6]:
        modules.append({"module": "module_A", "feature": f})
    for f in features[6:]:
        modules.append({"module": "module_B", "feature": f})
    pd.DataFrame(modules).to_csv(outdir / "toy_modules.tsv", sep="\t", index=False)

    network_a = np.eye(6)
    network_a[0, 1] = network_a[1, 0] = 1
    network_a[1, 2] = network_a[2, 1] = 1
    pd.DataFrame(network_a).to_csv(outdir / "toy_network_module_A.tsv", sep="\t", index=False, header=False)

    print(f"Wrote toy benchmark to {outdir}")


if __name__ == "__main__":
    main()
