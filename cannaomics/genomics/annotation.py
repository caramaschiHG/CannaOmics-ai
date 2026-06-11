"""Gene annotation mapping for variants."""


import pandas as pd

from .genes import GeneCatalog


def annotate_nearest_gene(
    variant_df: pd.DataFrame, gene_catalog: GeneCatalog, window_bp: int = 50000
) -> pd.DataFrame:
    """
    Annotate variants with their nearest gene.

    For the MVP, this relies on a heuristic based on feature names,
    simulating what an actual genomic mapping pipeline would do.

    Parameters
    ----------
    variant_df : pd.DataFrame
        DataFrame of variant features.
    gene_catalog : GeneCatalog
        The loaded gene catalog.
    window_bp : int, optional
        Window size in base pairs (simulated parameter for MVP).

    Returns
    -------
    pd.DataFrame
        The input DataFrame unmodified (since we use column names directly for the demo),
        but in a real implementation this would map genomic coordinates to genes.
    """
    # In a real pipeline, this would:
    # 1. Load VCF
    # 2. Load GFF
    # 3. Use interval trees to map variant coordinates to gene coordinates
    # 4. Return an annotated DataFrame or save to DB.

    # For the MVP, our synthetic features are pre-named
    # (e.g., 'TPS_region_snp_001'). We simulate the output.
    return variant_df


def classify_variant_region(variant_id: str, gene_catalog: GeneCatalog) -> str:
    """
    Classify a variant's genomic region relative to a gene.

    Parameters
    ----------
    variant_id : str
        The variant identifier.
    gene_catalog : GeneCatalog
        The catalog to check against.

    Returns
    -------
    str
        Region classification: 'intergenic', 'upstream', 'downstream', 'intron', 'exon', 'utr'.
    """
    # Simulated logic for MVP based on variant_id string
    vid_lower = variant_id.lower()

    if "exon" in vid_lower:
        return "exon"
    elif "intron" in vid_lower:
        return "intron"
    elif "utr" in vid_lower:
        return "utr"
    elif "intergenic" in vid_lower:
        return "intergenic"
    else:
        # Default assumption for 'region' snps in the demo
        return "upstream"
