"""Visualization utilities for interpretability."""

from pathlib import Path
from typing import Any

import pandas as pd

from ..utils.logging import get_logger

logger = get_logger("interpretability_plots")

try:
    import plotly.express as px

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("plotly is not installed. Plotting functions will fail.")


def plot_feature_importance(
    importance_df: pd.DataFrame, top_n: int = 20, output_path: Path | None = None
) -> Any:
    """
    Plot permutation feature importance.

    Parameters
    ----------
    importance_df : pd.DataFrame
        DataFrame from compute_permutation_importance.
    top_n : int, optional
        Number of features to plot.
    output_path : Path, optional
        Path to save HTML plot.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    if not PLOTLY_AVAILABLE:
        raise ImportError("plotly is required for plotting.")

    df_plot = importance_df.head(top_n).sort_values("importance_mean", ascending=True)

    fig = px.bar(
        df_plot,
        x="importance_mean",
        y="feature",
        error_x="importance_std",
        orientation="h",
        title=f"Top {top_n} Features by Permutation Importance",
        labels={
            "importance_mean": "Mean Decrease in Accuracy (Importance)",
            "feature": "Feature",
        },
        color="importance_mean",
        color_continuous_scale="Viridis",
    )

    fig.update_layout(height=max(400, top_n * 25), template="plotly_white")

    if output_path:
        fig.write_html(str(output_path))

    return fig


def plot_shap_summary(shap_result: Any, output_path: Path | None = None):
    """
    Generate a SHAP summary plot.
    Note: SHAP's native plots use matplotlib. This wraps it.
    """
    try:
        import matplotlib.pyplot as plt
        import shap

        # Native SHAP summary plot (matplotlib)
        plt.figure(figsize=(10, 8))
        shap.summary_plot(
            shap_result.shap_values, feature_names=shap_result.feature_names, show=False
        )

        if output_path:
            plt.savefig(str(output_path), bbox_inches="tight", dpi=300)
            plt.close()

    except ImportError:
        logger.error("shap and/or matplotlib not available for SHAP summary plot.")
    except Exception as e:
        logger.error(f"Failed to generate SHAP plot: {e}")
