
"""
01_count_papers.py

Counts PDF papers in a given folder.

Usage:
    python 01_count_papers.py
    python 01_count_papers.py --folder Initial_downloaded_papers
    python 01_count_papers.py --folder included
    python 01_count_papers.py --folder "D:\\full\\path\\to\\any\\folder"

If --folder is just a bare name (no slashes), the script looks for it
inside pdf_library/ (one level above this scripts/ folder). If --folder
is a full or relative path, it is used exactly as given.
"""

import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PDF_LIBRARY = PROJECT_ROOT / "pdf_library"


def resolve_folder(folder_arg: str) -> Path:
    p = Path(folder_arg)
    if len(p.parts) == 1:  # bare name, e.g. "included"
        return PDF_LIBRARY / folder_arg
    return p


def count_pdfs(folder: Path) -> int:
    return len([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"])


def main():
    parser = argparse.ArgumentParser(description="Count PDF papers in a folder.")
    parser.add_argument(
        "--folder",
        default="Initial_downloaded_papers",
        help="Folder name (inside pdf_library/) or a full/relative path. "
             "Default: Initial_downloaded_papers",
    )
    args = parser.parse_args()

    folder = resolve_folder(args.folder)

    if not folder.exists() or not folder.is_dir():
        print(f"Folder not found: {folder}")
        return

    total = count_pdfs(folder)
    print(f"Folder: {folder}")
    print(f"Total papers found: {total}")


if __name__ == "__main__":
    main()
