
"""
03_rename.py

Renames PDF papers inside pdf_library/included/ (by default) to a
sequential pattern of your choosing — e.g. p1, p2, p3, ... or
p100, p101, p102, ...

You can pass --prefix and --start on the command line, or leave them out
and the script will ask you interactively.

Usage:
    python 03_rename.py
    python 03_rename.py --folder included --prefix p --start 100
    python 03_rename.py --folder included --prefix paper_ --start 1
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


def find_pdfs(folder: Path):
    return sorted([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"])


def rename_papers(folder: Path, prefix: str, start: int):
    files = find_pdfs(folder)
    if not files:
        print("No PDF files found to rename.")
        return

    # Pass 1: rename everything to unique temp names first, so nothing
    # collides mid-process (e.g. renaming p2 -> p3 while p3 still exists).
    temp_paths = []
    for i, file in enumerate(files):
        temp_path = file.parent / f"__tmp_rename_{i}__.pdf"
        file.rename(temp_path)
        temp_paths.append(temp_path)

    # Pass 2: rename temp files to the final names.
    for i, temp_path in enumerate(temp_paths):
        new_name = f"{prefix}{start + i}.pdf"
        new_path = temp_path.parent / new_name
        temp_path.rename(new_path)
        print(f"  Renamed -> {new_name}")

    print(f"\nRenamed {len(files)} paper(s): {prefix}{start} .. {prefix}{start + len(files) - 1}")


def main():
    parser = argparse.ArgumentParser(description="Rename PDFs in a folder to a sequential pattern.")
    parser.add_argument(
        "--folder",
        default="included",
        help="Folder name (inside pdf_library/) or path containing PDFs to rename. Default: included",
    )
    parser.add_argument("--prefix", default=None, help="Prefix for renamed files, e.g. 'p' -> p100.pdf")
    parser.add_argument("--start", type=int, default=None, help="Starting number, e.g. 100 -> p100")
    args = parser.parse_args()

    folder = resolve_folder(args.folder)
    if not folder.exists() or not folder.is_dir():
        print(f"Folder not found: {folder}")
        return

    prefix = args.prefix
    start = args.start

    if prefix is None:
        prefix = input("Enter prefix for filenames (e.g. 'p' for p1.pdf): ").strip() or "p"

    if start is None:
        while True:
            raw = input("Enter starting number (e.g. 1 or 100): ").strip()
            try:
                start = int(raw)
                break
            except ValueError:
                print("Please enter a valid integer.")

    confirm = input(
        f"\nThis will rename all PDFs in '{folder}' to {prefix}{start}, {prefix}{start + 1}, ... "
        f"Proceed? (yes/no): "
    ).strip().lower()

    if confirm not in ("yes", "y"):
        print("Cancelled.")
        return

    rename_papers(folder, prefix, start)


if __name__ == "__main__":
    main()
