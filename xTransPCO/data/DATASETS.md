# Public benchmark datasets for TANGO vs trans-PCO

This document records public datasets that can be used to benchmark TANGO against original trans-PCO, PC1, MinP, and variance-component tests.

Large xQTL summary-statistics files should **not** be committed to GitHub. They are often too large for GitHub and may have dataset-specific usage terms. This repository should store:

1. dataset manifest files;
2. download scripts;
3. checksums when available;
4. preprocessing scripts;
5. tiny toy data for unit tests.

Raw large files should be stored under a local or cluster path such as:

```text
/data/public_xqtl/
```

or ignored local project path:

```text
xTransPCO/data/raw/
```

## Priority 1: eQTLGen trans-eQTL summary statistics

Purpose:

- Primary benchmark for expression-level trans-QTL module mapping.
- Suitable for comparing TANGO with original trans-PCO because original trans-PCO also used eQTLGen and DGN-style blood expression resources.

Why useful:

- Contains trans-eQTL results for approximately 10,000 known genetic risk variants.
- Provides significant and full trans-eQTL summary statistics.
- Has SNP-gene Z scores, which can be transformed into SNP-by-gene module input.

Files:

```text
2018-09-04-trans-eQTLsFDR-CohortInfoRemoved-BonferroniAdded.txt.gz
README_trans
```

Source page:

```text
https://www.eqtlgen.org/trans-eqtls.html
```

Direct full trans-eQTL file URL:

```text
https://download.gcc.rug.nl/downloads/eqtlgen/trans-eqtl/2018-09-04-trans-eQTLsFDR-CohortInfoRemoved-BonferroniAdded.txt.gz
```

## Priority 2: eQTLGen cis-eQTL summary statistics

Purpose:

- Mediator annotation for candidate trans loci.
- Used to test whether trans signals have nearby cis-eQTL support.

Files:

```text
2019-12-11-cis-eQTLsFDR-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz
README_cis
```

Source page:

```text
https://www.eqtlgen.org/cis-eqtls.html
```

Direct full cis-eQTL file URL:

```text
https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/2019-12-11-cis-eQTLsFDR-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz
```

## Priority 3: GTEx v8 single-tissue eQTL summary statistics

Purpose:

- Tissue-specific cis-eQTL annotation.
- Cross-tissue robustness test.
- Can help build tissue-relevant mediator priors.

Source page:

```text
https://gtexportal.org/home/downloads/adult-gtex/qtl
```

Notes:

- GTEx Portal is JavaScript based, so direct automated download URLs can change.
- Prefer using official GTEx Portal download instructions or Google Cloud bucket links from the portal.
- Respect GTEx usage terms.

## Priority 4: UKB-PPP pQTL summary statistics

Purpose:

- Protein-level benchmark.
- Useful for testing network or PPI-informed components of TANGO.

Source portal:

```text
http://ukb-ppp.gwas.eu
```

Notes:

- The UKB-PPP Nature paper reports proteomic profiling of 54,219 UK Biobank participants and pQTL mapping for thousands of proteins.
- The paper states that proteo-genomic results and summary association data are available through the interactive portal.
- Download may require portal-specific steps rather than a stable direct file URL.

## Priority 5: GoDMC or eGTEx mQTL summary statistics

Purpose:

- Methylation-level benchmark.
- Useful for extending TANGO beyond expression and protein QTLs.

Notes:

- Use if download access and file format are straightforward.
- For the first benchmark, eQTLGen trans-eQTL should be prioritized before mQTL data.

## Priority 6: PPI and pathway modules

Purpose:

- Required for the network-smoothed component.
- Can be used as fixed gene/protein modules.

Candidate resources:

- STRING protein-protein interaction network.
- Reactome pathways.
- CORUM protein complexes.
- MSigDB Hallmark / C2 curated gene sets.
- GO biological process gene sets.

Storage recommendation:

- Do not commit large full databases.
- Commit only module definitions used for benchmark or download scripts.

## Recommended first benchmark dataset

Start with eQTLGen trans-eQTL summary statistics because it is the most directly aligned with original trans-PCO.

Minimal benchmark input:

```text
SNP Gene Z-score P-value
```

Then build:

```text
SNP x gene Z-score matrix
module list
module-specific correlation matrix estimated from null SNPs
```

Benchmark methods:

1. PC1 test;
2. MinP;
3. variance-component test;
4. original PCO if available;
5. TANGO.
