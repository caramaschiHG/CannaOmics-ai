"""Gene-level feature aggregation for variant data.

This module provides utilities for aggregating variant-level features into
gene-level, window-level, and pathway-level representations to reduce
dimensionality and improve biological interpretability.
"""

from __future__ import annotations

import logging
from typing import Literal

import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_by_gene(
    variant_df: pd.DataFrame,
    gene_annotations: pd.DataFrame,
    method: Literal["count", "mean", "presence"] = "count",
) -> pd.DataFrame:
    """Aggregate variant-level features into gene-level features.

    Each variant column is mapped to its parent gene via
    ``gene_annotations``, then aggregated per gene using the chosen
    method.

    Parameters
    ----------
    variant_df : pd.DataFrame
        Variant feature matrix with samples as rows and variant IDs as
        columns.  Values are typically genotype encodings (0/1/2).
    gene_annotations : pd.DataFrame
        Mapping table with at least two columns: ``'variant_id'`` and
        ``'gene_id'``.  Each row maps a variant to the gene it belongs to.
    method : {'count', 'mean', 'presence'}, optional
        Aggregation method:

        - ``'count'``: sum of non-reference alleles per gene.
        - ``'mean'``: mean genotype value per gene.
        - ``'presence'``: binary flag (1 if any variant is non-zero).

        Default is ``'count'``.

    Returns
    -------
    pd.DataFrame
        Gene-level feature matrix (samples × genes).

    Raises
    ------
    ValueError
        If ``gene_annotations`` lacks required columns or ``method`` is
        unknown.
    """
    required_cols = {"variant_id", "gene_id"}
    if not required_cols.issubset(gene_annotations.columns):
        raise ValueError(
            f"gene_annotations must contain columns {required_cols}. "
            f"Found: {set(gene_annotations.columns)}"
        )

    # Build variant-to-gene mapping for variants present in variant_df
    variant_to_gene = gene_annotations.set_index("variant_id")["gene_id"]
    mapped_variants = variant_df.columns.intersection(variant_to_gene.index)
    unmapped = set(variant_df.columns) - set(mapped_variants)

    if len(unmapped) > 0:
        logger.warning(
            "%d variants have no gene annotation and will be excluded.",
            len(unmapped),
        )

    if len(mapped_variants) == 0:
        raise ValueError(
            "No variants in variant_df could be mapped to genes. "
            "Check that variant_id values in gene_annotations match "
            "column names in variant_df."
        )

    subset = variant_df[mapped_variants]
    gene_groups: dict[str, list[str]] = {}
    for variant_id in mapped_variants:
        gene_id = variant_to_gene[variant_id]
        gene_groups.setdefault(gene_id, []).append(variant_id)

    logger.info(
        "Aggregating %d variants into %d genes using method='%s'",
        len(mapped_variants),
        len(gene_groups),
        method,
    )

    gene_features: dict[str, pd.Series] = {}

    for gene_id, variants in gene_groups.items():
        gene_data = subset[variants]

        if method == "count":
            gene_features[gene_id] = gene_data.sum(axis=1)
        elif method == "mean":
            gene_features[gene_id] = gene_data.mean(axis=1)
        elif method == "presence":
            gene_features[gene_id] = (gene_data > 0).any(axis=1).astype(int)
        else:
            raise ValueError(
                f"Unknown aggregation method '{method}'. "
                "Choose from 'count', 'mean', 'presence'."
            )

    result = pd.DataFrame(gene_features, index=variant_df.index)
    logger.info("Gene feature matrix: %d samples × %d genes", *result.shape)

    return result


def compute_gene_window_features(
    variant_df: pd.DataFrame,
    gene_catalog: pd.DataFrame,
    window_bp: int = 50_000,
) -> pd.DataFrame:
    """Compute features per gene window (gene body ± flanking region).

    For each gene in the catalog, all variants falling within
    ``[gene_start - window_bp, gene_end + window_bp]`` on the same
    chromosome are counted.

    Parameters
    ----------
    variant_df : pd.DataFrame
        Variant feature matrix.  Column names must encode genomic
        positions in the format ``'chr_position'`` (e.g.,
        ``'chr1_12345'``).
    gene_catalog : pd.DataFrame
        Gene annotations with columns ``'gene_id'``, ``'chrom'``,
        ``'start'``, ``'end'``.
    window_bp : int, optional
        Number of base-pairs to extend each gene boundary.  Default is
        ``50000``.

    Returns
    -------
    pd.DataFrame
        Gene-window feature matrix (samples × genes) where each value is
        the sum of variant alleles within the window.

    Raises
    ------
    ValueError
        If ``gene_catalog`` is missing required columns.
    """
    required_cols = {"gene_id", "chrom", "start", "end"}
    if not required_cols.issubset(gene_catalog.columns):
        raise ValueError(
            f"gene_catalog must contain columns {required_cols}. "
            f"Found: {set(gene_catalog.columns)}"
        )

    # Parse variant positions from column names (format: chr_position)
    variant_positions: list[tuple[str, int, str]] = []
    for col in variant_df.columns:
        parts = str(col).split("_", maxsplit=1)
        if len(parts) == 2:
            try:
                chrom = parts[0]
                pos = int(parts[1])
                variant_positions.append((chrom, pos, col))
            except ValueError:
                continue

    if not variant_positions:
        logger.warning(
            "No variant columns matched 'chr_position' format. "
            "Returning empty DataFrame."
        )
        return pd.DataFrame(index=variant_df.index)

    # Build a lookup: chrom -> sorted list of (pos, col_name)
    chrom_variants: dict[str, list[tuple[int, str]]] = {}
    for chrom, pos, col in variant_positions:
        chrom_variants.setdefault(chrom, []).append((pos, col))
    for chrom in chrom_variants:
        chrom_variants[chrom].sort(key=lambda x: x[0])

    gene_window_features: dict[str, pd.Series] = {}

    for _, gene_row in gene_catalog.iterrows():
        gene_id = gene_row["gene_id"]
        chrom = str(gene_row["chrom"])
        start = int(gene_row["start"]) - window_bp
        end = int(gene_row["end"]) + window_bp

        if chrom not in chrom_variants:
            gene_window_features[gene_id] = pd.Series(
                0, index=variant_df.index, dtype=int
            )
            continue

        # Collect variants in window
        window_cols = [col for pos, col in chrom_variants[chrom] if start <= pos <= end]

        if window_cols:
            gene_window_features[gene_id] = variant_df[window_cols].sum(axis=1)
        else:
            gene_window_features[gene_id] = pd.Series(
                0, index=variant_df.index, dtype=int
            )

    result = pd.DataFrame(gene_window_features, index=variant_df.index)
    logger.info(
        "Gene-window features: %d samples × %d genes (window=%d bp)",
        *result.shape,
        window_bp,
    )

    return result


def compute_pathway_features(
    gene_features: pd.DataFrame,
    pathway_map: dict[str, list[str]],
) -> pd.DataFrame:
    """Aggregate gene-level features into pathway-level features.

    For each pathway, the feature value is the sum of constituent gene
    features.

    Parameters
    ----------
    gene_features : pd.DataFrame
        Gene-level feature matrix (samples × genes).
    pathway_map : dict[str, list[str]]
        Mapping from pathway name to list of gene IDs belonging to
        that pathway.

    Returns
    -------
    pd.DataFrame
        Pathway-level feature matrix (samples × pathways).
    """
    pathway_features: dict[str, pd.Series] = {}

    for pathway_name, gene_list in pathway_map.items():
        present_genes = [g for g in gene_list if g in gene_features.columns]

        if not present_genes:
            logger.debug(
                "Pathway '%s': no constituent genes found in features.",
                pathway_name,
            )
            pathway_features[pathway_name] = pd.Series(
                0, index=gene_features.index, dtype=float
            )
            continue

        pathway_features[pathway_name] = gene_features[present_genes].sum(axis=1)
        logger.debug(
            "Pathway '%s': aggregated %d / %d genes.",
            pathway_name,
            len(present_genes),
            len(gene_list),
        )

    result = pd.DataFrame(pathway_features, index=gene_features.index)
    logger.info("Pathway features: %d samples × %d pathways", *result.shape)

    return result
