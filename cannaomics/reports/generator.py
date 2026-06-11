"""Report generator."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import jinja2
import pandas as pd

from cannaomics import __version__

from ..utils.logging import get_logger
from .templates import MARKDOWN_TEMPLATE

logger = get_logger("report_generator")


class ReportGenerator:
    """Generates analysis reports from pipeline results."""

    def __init__(self, run_id: str, output_dir: Path):
        self.run_id = run_id
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup Jinja2 environment
        self.env = jinja2.Environment(autoescape=False, keep_trailing_newline=True)

    def generate_markdown(
        self,
        target: str,
        n_samples: int,
        n_features: int,
        model_name: str,
        metrics: dict[str, float],
        candidates_df: pd.DataFrame,
    ) -> Path:
        """Generate a Markdown report and write it to ``self.output_dir``."""
        template = self.env.from_string(MARKDOWN_TEMPLATE)

        # Prepare data
        top_candidates = candidates_df.head(10).to_dict(orient="records")

        rendered = template.render(
            run_id=self.run_id,
            target=target,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            n_samples=n_samples,
            n_features=n_features,
            model_name=model_name,
            metrics=metrics,
            top_candidates=top_candidates,
            version=__version__,
        )

        report_path = self.output_dir / f"report_{self.run_id}.md"
        report_path.write_text(rendered, encoding="utf-8")

        logger.info("Markdown report generated at %s", report_path)
        return report_path
