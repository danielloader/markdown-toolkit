import glob
from pathlib import Path

import anybadge
from pylint.lint import Run

THIS_FOLDER = Path(__file__).parent

thresholds = {8: "red", 9: "orange", 9.5: "yellow", 9.8: "green"}


def pylint(badge_path: str):
    """Generate Pylint badge for documentation.

    Args:
        badge_path (str): Path to write svg.
    """
    results = Run(
        glob.glob(str(THIS_FOLDER / ".." / "markdown_toolkit/*.py")),
        do_exit=False,
    )
    badge = anybadge.Badge(
        "pylint",
        f"{round(results.linter.stats.global_note, 2):.2f}",
        thresholds=thresholds,
    )
    badge.write_badge(str(THIS_FOLDER / ".." / badge_path), overwrite=True)


pylint("docs/img/badge-pylint.svg")
