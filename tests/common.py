from pathlib import Path


def resource_path(relative_path: str | Path | None = None) -> Path:
    res = (Path(__file__).parent / "resources").resolve()
    if relative_path is None:
        return res
    return res / relative_path
