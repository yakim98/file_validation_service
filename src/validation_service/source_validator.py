from __future__ import annotations

from typing import List, Dict, Any
from pathlib import Path
import csv

from .file_utils import load_yaml_config, validate_type
from .report_writer import write_report
from .logger import get_logger
from .config_paths import (
    SOURCE_CONFIG_PATH,
    SOURCE_DATA_PATH,
    SOURCE_VALIDATION_REPORT_FILE_PATH
)

logger = get_logger(__name__)

def source_validator(config_path: Path = SOURCE_CONFIG_PATH) -> None:
    source_config = load_yaml_config(config_path)
    folders_config: List[Dict[str, Any]] = source_config.get('folders')

    list_errors: List[Dict[str, Any]] = []

    for folder in folders_config:
        folder_name = folder.get('name')
        folder_path = SOURCE_DATA_PATH / folder_name
        files_config = folder.get('files')
        for file_cnfg in files_config:
            file_name = file_cnfg.get('name')
            expected_columns = file_cnfg.get('columns', {})
            file_path = folder_path / file_name

            try:
                with open(file_path) as file:
                    reader = csv.DictReader(file)

                    for row_number, row in enumerate(reader, start=2):
                        for column, expected_type in expected_columns.items():
                            value = row.get(column)
                            if not validate_type(value, expected_type):
                                list_errors.append({
                                    "error_level": "error",
                                    "error_text": f'Wrong datatype for the column "{column}"',
                                    "file_name": file_name,
                                    "folder_name": str(folder_path),
                                    "line_number": row_number
                                })
            except csv.Error:
                logger.exception(f"CSV parsing failed: {file_path}")
                list_errors.append({
                    "error_level": "error",
                    "error_text": f"Failed to parse CSV file {file_name}",
                    "file_name": file_name,
                    "folder_name": str(folder_path),
                    "line_number": row_number
                })

    write_report(list_errors, SOURCE_VALIDATION_REPORT_FILE_PATH, encoding = source_config.get('encoding', 'utf-8'))
    logger.info(f'SOURCE validation completed. {len(list_errors)} errors/warnings found')

if __name__ == "__main__":
    source_validator(SOURCE_CONFIG_PATH)



