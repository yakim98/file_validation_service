from pathlib import Path
from typing import Iterator, List
import fnmatch

def list_files(folder: Path, patterns: List[str]) -> Iterator[Path]:
    if not folder.exists():
        return iter(())
    for element in folder.iterdir():
        if not element.is_file():
            continue
        for pattern in patterns:
            if fnmatch.fnmatch(element.name, pattern):
                yield element

def is_csv_file(path: Path) -> bool:
    return path.suffix.lower() == ".csv"