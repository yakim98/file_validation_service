from __future__ import annotations
from pathlib import Path
from typing import Iterable, Dict, Any
import csv

from .logger import get_logger

logger = get_logger(__name__)

DEFAULT_HEADERS = ["error_level", "error_text", "file_name", "folder_name", "line_number"]

def write_report(list_errors: Iterable[Dict[str, Any]], output_path: Path, encoding = 'utf-8') -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', newline='', encoding=encoding) as file:
        writer = csv.DictWriter(file, fieldnames=DEFAULT_HEADERS)
        writer.writeheader()
        for error in list_errors:
            row = {key: error.get(key, '') for key in DEFAULT_HEADERS}
            writer.writerow(row)
    logger.info(f'Wrote report to {output_path}')