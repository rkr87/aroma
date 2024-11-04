"""TODO."""

import zipfile
from pathlib import Path


def zip_directory_contents(source_dir: Path, output_zip: Path) -> None:
    """TODO."""
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(source_dir))


if __name__ == "__main__":
    source_directory = Path.cwd() / "src"
    output_zip_path = Path.cwd() / "aroma.zip"
    zip_directory_contents(source_directory, output_zip_path)
