"""Candidate ranking and biological context generation."""


import pandas as pd

from ..genomics.annotation import classify_variant_region
from ..genomics.genes import GeneCatalog


def rank_candidates(
    importance_df: pd.DataFrame,
    shap_df: pd.DataFrame | None,
    gene_catalog: GeneCatalog,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Rank genomic features based on ML importance and annotate with biology.

    Parameters
    ----------
    importance_df : pd.DataFrame
        DataFrame from compute_permutation_importance.
    shap_df : pd.DataFrame, optional
        DataFrame from get_top_shap_features.
    gene_catalog : GeneCatalog
        Catalog for biological annotation.
    top_n : int, optional
        Number of top candidates to return.

    Returns
    -------
    pd.DataFrame
        Ranked and annotated candidate list.
    """
    if importance_df.empty:
        return pd.DataFrame()

    # Start with base importance
    candidates = importance_df.head(max(top_n * 2, 100)).copy()

    # Merge SHAP if available
    if shap_df is not None and not shap_df.empty:
        candidates = candidates.merge(shap_df, on="feature", how="left")

        # Combined score heuristic (simple average of ranks if we had them,
        # or just sort by SHAP where available, then importance)
        candidates["combined_score"] = candidates["importance_mean"]
        if "mean_abs_shap" in candidates.columns:
            # Normalize and combine
            imp_norm = (
                candidates["importance_mean"] / candidates["importance_mean"].max()
            )
            shap_norm = candidates["mean_abs_shap"].fillna(0)
            if shap_norm.max() > 0:
                shap_norm = shap_norm / shap_norm.max()
            candidates["combined_score"] = imp_norm * 0.5 + shap_norm * 0.5

        candidates = candidates.sort_values("combined_score", ascending=False).head(
            top_n
        )
    else:
        candidates = candidates.head(top_n)

    # Add biological annotations
    candidates["candidate_type"] = candidates["feature"].apply(
        lambda f: (
            "gene_expression" if "exp_" in f else "variant" if "snp" in f else "other"
        )
    )

    # Simulate annotation for MVP based on feature names
    annotated_genes = []
    regions = []

    for feature in candidates["feature"]:
        # Attempt to extract gene name from feature (e.g. 'CsTPS1_exp' -> 'CsTPS1')
        gene_name = feature.split("_")[0]
        gene_info = gene_catalog.search(gene_name)

        if gene_info:
            annotated_genes.append(gene_info[0].gene_id)
        else:
            # Maybe it's a generic region
            if "TPS" in feature:
                annotated_genes.append("TPS_Family")
            else:
                annotated_genes.append("Unknown")

        regions.append(classify_variant_region(feature, gene_catalog))

    candidates["nearest_gene"] = annotated_genes
    candidates["genomic_region"] = regions

    return candidates.reset_index(drop=True)
