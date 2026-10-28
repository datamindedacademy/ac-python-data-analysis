"""Check the exercises and solutions: every exercises/*/exercise.ipynb is clean, and every
solutions/*/solution.ipynb runs without errors.

Run it from the root of the repository, after `uv run python generate_data.py`:

    uv run python check_notebooks.py             # all solutions, except the API exercise
    uv run python check_notebooks.py --with-api  # also the API exercise, which needs the internet

The solutions are run in memory: the notebooks on disk do not change. A cell that fails on purpose has the
tag `raises-exception`.
"""

import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).parent
NEEDS_INTERNET = {"09-fetching-from-an-api"}


def name(path: Path) -> str:
    """The path of a notebook relative to the root of the repository, for messages."""
    return str(path.relative_to(ROOT))


def main() -> int:
    with_api = "--with-api" in sys.argv
    exercises = sorted(ROOT.glob("exercises/[0-9][0-9]-*/exercise.ipynb"))
    solutions = sorted(ROOT.glob("solutions/[0-9][0-9]-*/solution.ipynb"))
    problems = []

    for path in exercises:
        exercise = nbformat.read(path, as_version=4)
        if any(
            cell.get("outputs") or cell.get("execution_count")
            for cell in exercise.cells
            if cell.cell_type == "code"
        ):
            problems.append(
                f"{name(path)} has outputs: clear them before committing"
            )

    for path in solutions:
        if path.parent.name in NEEDS_INTERNET and not with_api:
            print(f"skipped  {name(path)} (needs the internet: --with-api)")
            continue
        solution = nbformat.read(path, as_version=4)
        client = NotebookClient(
            solution, timeout=600, resources={"metadata": {"path": str(path.parent)}}
        )
        try:
            # The kernel's own warnings on stderr are noise; errors in cells still come through the client
            client.execute(stderr=subprocess.DEVNULL)
            print(f"ok       {name(path)}")
        except CellExecutionError as error:
            problems.append(
                f"{name(path)} fails:\n{str(error)[-1500:]}"
            )
            print(f"FAILED   {name(path)}")

    for problem in problems:
        print("\n" + problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
