"""Utility script to zip the current directory and all subdirectories.

The archive is created with relative paths so the structure is preserved when
unzipped. The output file is skipped during compression to avoid including the
archive itself when it is created inside the target directory.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile


def zip_directory(base_dir: Path, output_file: Path) -> None:
    """Zip ``base_dir`` and all its contents into ``output_file``.

    Args:
        base_dir: Directory whose contents should be archived.
        output_file: Path to the zip archive to create.
    """
    base_dir = base_dir.resolve()
    output_file = output_file.resolve()

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for path in base_dir.rglob("*"):
            # Avoid adding the archive itself if it resides within ``base_dir``.
            if path.resolve() == output_file:
                continue
            zipf.write(path, path.relative_to(base_dir))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zip the current directory and its subdirectories.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path.cwd().name + ".zip",
        help="Output zip file path. Defaults to '<current_dir>.zip' in the current directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    zip_directory(Path.cwd(), args.output)


if __name__ == "__main__":
    main()
