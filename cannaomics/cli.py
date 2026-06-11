"""Command-line interface for CannaOmics AI.

Provides a Typer-based CLI with Rich output for running cannabis
genotype-to-chemotype analysis pipelines.

Usage
-----
.. code-block:: bash

    cannaomics --help
    cannaomics demo
    cannaomics run --config pipeline.yaml
    cannaomics train --config pipeline.yaml --target beta_myrcene
    cannaomics report --run-id abc123
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from cannaomics import __version__

# ---------------------------------------------------------------------------
# Windows console hardening
# ---------------------------------------------------------------------------
# Windows defaults stdout to cp1252, which crashes on non-BMP unicode (e.g.
# the 🧬 emoji used in CLI panels). Force UTF-8 when available so help text
# and rich panels render consistently across platforms.
if sys.platform == "win32":  # pragma: no cover - platform-specific
    for _stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(AttributeError, ValueError):
            _stream.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Console & application
# ---------------------------------------------------------------------------

console = Console(
    # Force VT100/ANSI rendering on Windows so non-BMP unicode (e.g. 🧬)
    # does not crash on legacy cp1252 consoles.
    legacy_windows=False if sys.platform == "win32" else None,
)

app = typer.Typer(
    name="cannaomics",
    help="CannaOmics AI - Cannabis sativa genotype-to-chemotype analysis.",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
)


# ---------------------------------------------------------------------------
# Version callback
# ---------------------------------------------------------------------------


def _version_callback(value: bool) -> None:
    """Print version and exit.

    Parameters
    ----------
    value : bool
        Whether the ``--version`` flag was passed.
    """
    if value:
        console.print(
            Panel(
                f"[bold cyan]CannaOmics AI[/]  v{__version__}",
                border_style="bright_green",
                expand=False,
            )
        )
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """CannaOmics AI - Cannabis sativa genotype-to-chemotype analysis."""


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


@app.command()
def demo() -> None:
    """Run the built-in demonstration pipeline.

    Generates synthetic data and walks through the full
    genotype-to-chemotype analysis workflow.
    """
    console.print(
        Panel(
            f"[bold cyan]CannaOmics AI[/]  v{__version__}\n"
            "[dim]Open-source framework for "
            "Cannabis genotype-to-chemotype analysis.[/]",
            border_style="cyan",
            expand=False,
        )
    )

    try:
        # Lazy import for fast CLI startup
        from cannaomics.demo import run_demo  # type: ignore[import-untyped]

        run_demo()
    except ImportError as exc:
        console.print(
            "[bold red]Error:[/] Demo module not yet installed. "
            "Run [bold]pip install cannaomics\\[demo][/] first."
        )
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(f"[bold red]Pipeline failed:[/] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def run(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        help="Path to YAML configuration file.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    """Run the full analysis pipeline from a YAML configuration file.

    Parameters
    ----------
    config : Path
        Path to a valid CannaOmics YAML configuration file.
    """
    console.print(
        Panel(
            f"[bold cyan]CannaOmics AI[/]  v{__version__}\n"
            f"[dim]Config:[/] {config}",
            border_style="bright_green",
            expand=False,
        )
    )

    try:
        # Lazy imports
        from cannaomics.config.schema import load_config

        pipeline_cfg = load_config(config)
        console.print(
            f"[green]OK[/] Configuration loaded: "
            f"[bold]{pipeline_cfg.project.name}[/]"
        )

        # Pipeline execution would be dispatched here
        console.print("[yellow]WARN[/] Full pipeline runner not yet implemented.")
    except Exception as exc:
        console.print(f"[bold red]Pipeline failed:[/] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def train(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        help="Path to YAML configuration file.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    target: str = typer.Option(
        ...,
        "--target",
        "-t",
        help="Target compound to train on (e.g. beta_myrcene, THC).",
    ),
) -> None:
    """Train a predictive model for a specific target compound.

    Parameters
    ----------
    config : Path
        Path to a valid CannaOmics YAML configuration file.
    target : str
        Name of the compound to predict (canonical or synonym).
    """
    console.print(
        Panel(
            f"[bold cyan]CannaOmics AI[/]  v{__version__}\n"
            f"[dim]Config:[/] {config}\n"
            f"[dim]Target:[/] {target}",
            border_style="bright_green",
            expand=False,
        )
    )

    try:
        from cannaomics.config.schema import load_config

        pipeline_cfg = load_config(config)
        console.print(
            f"[green]OK[/] Configuration loaded: "
            f"[bold]{pipeline_cfg.project.name}[/]"
        )
        console.print(f"[green]OK[/] Target compound: [bold]{target}[/]")

        # Model training would be dispatched here
        console.print("[yellow]WARN[/] Model trainer not yet implemented.")
    except Exception as exc:
        console.print(f"[bold red]Training failed:[/] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def report(
    run_id: str | None = typer.Option(
        None,
        "--run-id",
        "-r",
        help="Unique identifier of a previous pipeline run.",
    ),
    results_dir: Path | None = typer.Option(
        None,
        "--results-dir",
        "-d",
        help="Path to directory containing pipeline results.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    """Generate a report from pipeline results.

    Provide either ``--run-id`` to look up a previous run or
    ``--results-dir`` to point directly at an output folder.

    Parameters
    ----------
    run_id : str, optional
        Identifier of a previous pipeline run.
    results_dir : Path, optional
        Directory containing pipeline outputs.
    """
    if run_id is None and results_dir is None:
        console.print("[bold red]Error:[/] Provide either --run-id or --results-dir.")
        raise typer.Exit(code=1)

    source = run_id if run_id else str(results_dir)
    console.print(
        Panel(
            f"[bold cyan]CannaOmics AI[/]  v{__version__}\n"
            f"[dim]Source:[/] {source}",
            border_style="bright_green",
            expand=False,
        )
    )

    try:
        # Report generation would be dispatched here
        console.print("[yellow]WARN[/] Report generator not yet implemented.")
    except Exception as exc:
        console.print(f"[bold red]Report generation failed:[/] {exc}")
        raise typer.Exit(code=1) from exc


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
