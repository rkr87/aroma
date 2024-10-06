"""TODO."""

from pathlib import Path

from data.source.archive_api import ArchiveAPISession


def download_archive_org_file(
    archive_id: str, archive_path: str, save_path: Path, *, auth_req: bool
) -> bool:
    """TODO.."""
    with ArchiveAPISession() as session:
        if (
            data := session.make_request(
                f"/download/{archive_id}{archive_path}", auth_req=auth_req
            )
        ) is None:
            return False
        with save_path.open(mode="wb") as f:
            f.write(data.content)
        return save_path.is_file()
