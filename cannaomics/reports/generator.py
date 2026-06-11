"""Report generator."""

from datetime import datetime
from pathlib import Path

import jinja2
import pandas as pd

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
        self.env = jinja2.Environment()

    def generate_markdown(
        self,
        target: str,
        n_samples: int,
        n_features: int,
        model_name: str,
        metrics: dict[str, float],
        candidates_df: pd.DataFrame,
    ) -> Path:
        """
        Generate a Markdown report.
        """
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
            version="0.1.0",
        )

        report_path = self.output_dir / f"report_{self.run_id}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        logger.info(f"Markdown report generated at {report_path}")
        return report_path
