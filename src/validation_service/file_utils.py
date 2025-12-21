from typing import Iterator, List
import fnmatch
from pathlib import Path
import yaml
import csv
from logger import get_logger

logger = get_logger(__name__)

def list_files(folder: Path, patterns: List[str]) -> Iterator[Path]:
    if not folder.exists():
        return iter(())
    for element in folder.iterdir():
        if not element.is_file():
            continue
        for pattern in patterns:
            if fnmatch.fnmatch(element.name, pattern):
                yield element

def is_csv_file(path: Path, encoding: str = "utf-8") -> bool:
    if path.suffix.lower() != ".csv":
        return False

    try:
        with open(path, "r", encoding=encoding, newline="") as f:
            sample = f.read(4096)
            if not sample.strip():
                return False

            csv.Sniffer().sniff(sample)
            return True

    except (OSError, UnicodeDecodeError, csv.Error):
        return False

def load_yaml_config(path: Path):
    try:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        logger.error(f"Config file file not found: {path}")
        raise