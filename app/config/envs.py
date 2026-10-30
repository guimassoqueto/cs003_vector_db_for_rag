from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MAX_TOKENS = 1024

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LESSONS_DIR = PROJECT_ROOT / "lessons"


def doc_path(script: str) -> Path:
    """Return the notes a lesson was written from: the .md file beside the script.

    lessons/module01/01_similarity_search.py
        -> lessons/module01/01_similarity_search.md

    Args:
        script: the calling script's __file__.
    """
    return Path(script).resolve().with_suffix(".md")


def output_path(script: str, filename: str) -> Path:
    """Return the path a lesson should write a generated file to.

    lessons/module01/01_similarity_search.py + "similarities.csv"
        -> lessons/module01/output/01_similarity_search/similarities.csv

    The parent directory is created if needed, so callers can write immediately.

    Args:
        script: the calling script's __file__.
        filename: name of the file to generate.
    """
    lesson = Path(script).resolve()
    path = lesson.parent / "output" / lesson.stem / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
