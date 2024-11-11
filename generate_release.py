"""TODO."""

import argparse
import zipfile
from pathlib import Path


def zip_directory_contents(source_dir: Path, output_zip: Path) -> None:
    """Compresses the contents of the source directory into a zip file."""
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(source_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Zip the contents of a directory."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / "aroma.zip",
        help="Output zip file path (default: aroma.zip)",
    )

    args = parser.parse_args()
    source_directory = Path.cwd() / "src"
    output_zip_path = args.output

    zip_directory_contents(source_directory, output_zip_path)
