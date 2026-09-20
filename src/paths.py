"""Repository-relative paths used by notebooks and source modules."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
RESULTS_DIR = PROJECT_ROOT / "results"
RUNTIME_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "runtime"
FIGURE_OUTPUT_DIR = RUNTIME_OUTPUT_DIR / "figures"


def ensure_runtime_directories() -> None:
    """Create only runtime output directories; never modify frozen inputs."""
    FIGURE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
