"""Demonstration pipeline script."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel

from .chemistry.chemotype import classify_samples
from .features.build_features import build_feature_matrix
from .genomics.genes import catalog
from .interpretability.candidate_ranking import rank_candidates
from .interpretability.feature_importance import compute_permutation_importance
from .interpretability.plots import plot_feature_importance, plot_shap_summary
from .interpretability.shap_analysis import compute_shap_values, get_top_shap_features
from .models.evaluate import evaluate_model, format_metrics_table
from .models.model_registry import ModelMetadata, save_model
from .models.train import train_model
from .reports.generator import ReportGenerator
from .utils.logging import get_logger

logger = get_logger("demo")
console = Console()


def run_demo(config_path: Path | None = None) -> None:
    """Run a complete end-to-end demonstration using synthetic data."""
    console.print(
        Panel.fit(
            "[bold green]CannaOmics AI - Demo Pipeline[/bold green]\n"
            "Running end-to-end genotype-to-chemotype analysis on synthetic data.",
            border_style="green",
        )
    )

    # 1. Loading Data
    console.print("[dim]Loading synthetic data...[/dim]")
    root = Path(__file__).parent.parent
    chem_path = root / "examples" / "mini_chemical_profile.csv"
    var_path = root / "examples" / "mini_variant_matrix.csv"

    chem_df = pd.read_csv(chem_path)
    var_df = pd.read_csv(var_path)
    console.print("[green]Data loaded![/green]")

    # 2. Chemistry Normalization & Chemotype Classification
    console.print("[dim]Classifying chemotypes...[/dim]")
    chem_df = classify_samples(chem_df)
    console.print("[green]Chemotypes classified![/green]")

    # 3. Feature Matrix Construction
    console.print("[dim]Building feature matrix...[/dim]")
    # Using build_feature_matrix directly to handle alignment and classification
    X, y = build_feature_matrix(
        variant_df=var_df.set_index("sample_id"),
        chemical_df=chem_df.set_index("sample_id"),
        target_compound="THC",
    )
    console.print("[green]Feature matrix built![/green]")

    console.print(
        f"Data shape: [bold cyan]{X.shape[0]} samples[/bold cyan] "
        f"x [bold cyan]{X.shape[1]} features[/bold cyan]"
    )

    # 4. Model Training
    console.print("[dim]Training Random Forest model...[/dim]")
    train_res = train_model(X, y, "random_forest", n_splits=3)
    console.print("[green]Model trained![/green]")

    # 5. Evaluation
    eval_res = evaluate_model(
        train_res.model, X, y
    )  # Evaluating on train for demo simplicity
    console.print(format_metrics_table(eval_res.to_dict(), "Demo Model Performance"))

    # 6. Interpretability (Feature Importance & SHAP)
    console.print("[dim]Computing feature importance & SHAP values...[/dim]")
    importance_df = compute_permutation_importance(train_res.model, X, y)
    shap_res = compute_shap_values(train_res.model, X)
    shap_df = get_top_shap_features(shap_res) if shap_res else None

    candidates_df = rank_candidates(importance_df, shap_df, catalog, top_n=5)
    console.print("[green]Interpretability analysis complete![/green]")

    console.print("\n[bold]Top Candidate Genomic Features[/bold]")
    console.print(
        candidates_df[["feature", "candidate_type", "nearest_gene", "combined_score"]]
    )

    # 7. Reporting & Saving
    console.print("[dim]Generating reports and saving models...[/dim]")
    out_dir = root / "results" / "demo_run"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save plots
    plot_feature_importance(importance_df, output_path=out_dir / "importance.html")
    if shap_res:
        plot_shap_summary(shap_res, output_path=out_dir / "shap_summary.png")

    # Generate Report
    generator = ReportGenerator("demo_001", out_dir)
    generator.generate_markdown(
        "chemotype",
        len(X),
        X.shape[1],
        "random_forest",
        eval_res.to_dict(),
        candidates_df,
    )

    # Save model
    meta = ModelMetadata(
        model_name="demo_rf",
        model_type="random_forest",
        target_compound="chemotype",
        n_features=X.shape[1],
        n_samples=len(X),
        metrics=eval_res.to_dict(),
        training_date=datetime.now().isoformat(timespec="seconds"),
    )
    save_model(train_res.model, meta, out_dir / "models")

    console.print("[green]Run artifacts saved![/green]")

    console.print(
        f"\n[bold green]Demo completed successfully![/bold green] "
        f"Results saved to [cyan]{out_dir}[/cyan]"
    )


if __name__ == "__main__":
    run_demo()
