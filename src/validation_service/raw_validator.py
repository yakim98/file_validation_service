from __future__ import annotations
from typing import List, Dict, Any
import csv
from pathlib import Path

from .file_utils import list_files, is_csv_file
from .report_writer import write_report
from .logger import get_logger

logger = get_logger(__name__)

def raw_validator(raw_config: dict,
                  base_path: Path,
                  report_path: Path
                  ) -> None:
    folders_config: List[Dict[str, Any]] = raw_config.get('folders')

    list_errors: List[Dict[str, Any]] = []

    for folder in folders_config:
        name = folder.get('name')
        if not name:
            list_errors.append(
                {
                    "error_level": "error",
                    "error_text": 'Folder "name" is missing in config',
                    "file_name": "",
                    "folder_name": "",
                    "line_number": ""
                }
            )
            continue
        folder_path = base_path / name
        if not folder_path.exists():
            list_errors.append(
                {
                    "error_level": "error",
                    "error_text": f"Required folder {name} is missing",
                    "file_name": "",
                    "folder_name": str(folder_path),
                    "line_number": ""
                }
            )
        else:
            logger.info(f"Folder found: {folder_path}")

            required_columns = folder.get('required_columns', [])
            if not isinstance(required_columns, list):
                list_errors.append(
                    {
                        "error_level": "error",
                        "error_text": f'Folder "{name}" has invalid or missing "required_columns"',
                        "file_name": "",
                        "folder_name": name,
                        "line_number": ""
                    }
                )
                continue
            files = list(list_files(folder_path, ["*"]))
            if not files:
                list_errors.append(
                    {
                        "error_level": "warning",
                        "error_text": f"Folder {name} does not contain any file",
                        "file_name": "",
                        "folder_name": str(folder_path),
                        "line_number": ""
                    }
                )
                continue

            for file_path in files:
                if not is_csv_file(file_path, encoding=raw_config.get("encoding", "utf-8")):
                    list_errors.append(
                        {
                            "error_level": "error",
                            "error_text": f"File {file_path.name} has unsupported format",
                            "file_name": file_path.name,
                            "folder_name": str(folder_path),
                            "line_number": ""
                        }
                    )
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        cols = next(reader)
                except StopIteration:
                    logger.exception(f'CSV file is empty: {file_path}')
                    list_errors.append(
                        {
                            "error_level": "error",
                            "error_text": f'CSV file is empty: {file_path.name}',
                            "file_name": file_path.name,
                            "folder_name": str(folder_path),
                            "line_number": ""
                        }
                    )
                    continue

                except csv.Error:
                    logger.exception(f'Failed to parse CSV header: {file_path}')
                    list_errors.append(
                        {
                            "error_level": "error",
                            "error_text": f'Failed to parse CSV header: {file_path.name}',
                            "file_name": file_path.name,
                            "folder_name": str(folder_path),
                            "line_number": ""
                        }
                    )
                    continue

                missing_columns = set(required_columns) - set(cols)
                for missing_col in missing_columns:
                    list_errors.append({
                        "error_level": "error",
                        "error_text": f'Required column "{missing_col}" is missing',
                        "file_name": file_path.name,
                        "folder_name": str(folder_path),
                        "line_number": ""
                    })

    write_report(list_errors, report_path, encoding=raw_config.get('encoding', 'utf-8'))
    logger.info(f'RAW validation completed. {len(list_errors)} errors/warnings found')
