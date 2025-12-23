from typing import Iterator, List
import fnmatch
from pathlib import Path
import yaml
import csv
from datetime import datetime
from .logger import get_logger
from .config_paths import CSV_SAMPLE_SIZE

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
            sample = f.read(CSV_SAMPLE_SIZE)
            if not sample.strip():
                return False

            csv.Sniffer().sniff(sample)
            return True

    except (OSError, UnicodeDecodeError, csv.Error):
        return False

def load_yaml_config(path: Path):
    with open(path, 'r') as file:
            config = yaml.safe_load(file)
            return config

def validate_type(value: str, expected_type: str) -> bool:
    if value is None or value == '':
        return False
    try:
        if expected_type.lower() in ('str', 'string', 'text'):
            str(value)
            return True
        elif expected_type.lower() in ('int', 'integer'):
            int(value)
            return True
        elif expected_type.lower() in ('float', 'double', 'decimal'):
            float(value)
            return True
        elif expected_type.lower() == "date":
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return True
        else:
            logger.warning(f'Unknown data type: {expected_type}')
            return False
    except (ValueError, AttributeError):
        return False