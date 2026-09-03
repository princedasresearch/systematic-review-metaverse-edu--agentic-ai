
"""
02_deduplicate.py

Scans pdf_library/Initial_downloaded_papers (or a folder you specify),
finds duplicate PDFs by comparing file content, and sorts them:

    - duplicate papers -> pdf_library/excluded/
    - unique papers    -> pdf_library/included/

By default files are COPIED (not moved) out of the source folder, so
Initial_downloaded_papers stays intact as your original download record.
Pass --move if you'd rather move them out instead of copying.

Usage:
    python 02_deduplicate.py
    python 02_deduplicate.py --source Initial_downloaded_papers
    python 02_deduplicate.py --move
"""

import argparse
import hashlib
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PDF_LIBRARY = PROJECT_ROOT / "pdf_library"


def resolve_folder(folder_arg: str) -> Path:
    p = Path(folder_arg)
    if len(p.parts) == 1:  # bare name, e.g. "Initial_downloaded_papers"
        return PDF_LIBRARY / folder_arg
    return p


def get_file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_pdfs(folder: Path):
    return sorted([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"])


def unique_dest(dest_folder: Path, filename: str) -> Path:
    dest = dest_folder / filename
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while dest.exists():
        dest = dest_folder / f"{stem}_{counter}{suffix}"
        counter += 1
    return dest


def main():
    parser = argparse.ArgumentParser(description="Find duplicate PDFs and sort into included/excluded.")
    parser.add_argument(
        "--source",
        default="Initial_downloaded_papers",
        help="Folder name (inside pdf_library/) or path containing papers to scan. "
             "Default: Initial_downloaded_papers",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files out of the source folder instead of copying them.",
    )
    args = parser.parse_args()

    source = resolve_folder(args.source)
    if not source.exists() or not source.is_dir():
        print(f"Source folder not found: {source}")
        return

    included_folder = PDF_LIBRARY / "included"
    excluded_folder = PDF_LIBRARY / "excluded"
    included_folder.mkdir(parents=True, exist_ok=True)
    excluded_folder.mkdir(parents=True, exist_ok=True)

    pdfs = find_pdfs(source)
    total = len(pdfs)
    print(f"Source folder: {source}")
    print(f"Total papers found: {total}\n")

    seen_hashes = {}
    duplicate_count = 0
    included_count = 0

    transfer = shutil.move if args.move else shutil.copy2
    verb = "Moved" if args.move else "Copied"

    for file in pdfs:
        file_hash = get_file_hash(file)
        if file_hash in seen_hashes:
            dest = unique_dest(excluded_folder, file.name)
            transfer(str(file), str(dest))
            duplicate_count += 1
            print(f"  [duplicate] {file.name} -> excluded/{dest.name}")
        else:
            seen_hashes[file_hash] = file
            dest = unique_dest(included_folder, file.name)
            transfer(str(file), str(dest))
            included_count += 1
            print(f"  [unique]    {file.name} -> included/{dest.name}")

    print()
    print(f"{verb} {duplicate_count} duplicate paper(s) to: {excluded_folder}")
    print(f"{verb} {included_count} unique paper(s) to: {included_folder}")
    print(f"Duplicate count: {duplicate_count}")


if __name__ == "__main__":
    main()
