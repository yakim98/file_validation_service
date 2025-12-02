from __future__ import annotations
from typing import List, Dict, Any
import pandas as pd

from file_utils import list_files, is_csv_file, load_yaml_config
from report_writer import write_report
from logger import get_logger
from config_paths import *

logger = get_logger(__name__)

EMPTY_STRING = ""

def raw_validator(config_path: Path = RAW_CONFIG_PATH) -> None:
    raw_config = load_yaml_config(config_path)
    base_path = RAW_DATA_PATH
    folders_config = raw_config.get('folders')

    list_errors: List[Dict[str, Any]] = []

    for folder in folders_config:
        name = folder.get('name')
        folder_path = base_path / name
        if not folder_path.exists():
            list_errors.append(
                {
                    "error_level": "error",
                    "error_text": f"Required folder {name} not found",
                    "file_name": EMPTY_STRING,
                    "folder_name": str(folder_path),
                    "line_number": EMPTY_STRING
                }
            )
        else:
            logger.info("Folder found:", folder_path)

            required_columns = folder.get('required_columns', [])
            files = list(list_files(folder_path, ["*"]))
            if not files:
                list_errors.append(
                    {
                        "error_level": "warning",
                        "error_text": f"Folder {name} doesn't contain any corresponding files",
                        "file_name": EMPTY_STRING,
                        "folder_name": str(folder_path),
                        "line_number": EMPTY_STRING
                    }
                )
                continue

            for file_path in files:
                if not is_csv_file(file_path):
                    list_errors.append(
                        {
                            "error_level": "error",
                            "error_text": f"File {file_path.name} has unsupported format",
                            "file_name": file_path.name,
                            "folder_name": str(folder_path),
                            "line_number": EMPTY_STRING
                        }
                    )
                    continue

                try:
                    df = pd.read_csv(file_path, nrows=0)
                    cols = list(df.columns)
                except Exception as e:
                    logger.exception(f'Failed to read CSV header {file_path}:', e)
                    list_errors.append(
                        {
                            "error_level": "error",
                            "error_text": f'Failed to read CSV header {file_path.name}. Error: {e}',
                            "file_name": file_path.name,
                            "folder_name": str(folder_path),
                            "line_number": EMPTY_STRING
                        }
                    )
                    continue

                for i, req in enumerate(required_columns):
                    if req not in cols:
                        if i < len(required_columns):
                            orig_req = required_columns[i]
                        else:
                            orig_req = req
                        list_errors.append(
                            {
                                "error_level": "error",
                                "error_text": f'Required column {orig_req} is missing',
                                "file_name": file_path.name,
                                "folder_name": str(folder_path),
                                "line_number": EMPTY_STRING
                            }
                        )

    write_report(list_errors, REPORT_FILE_PATH, encoding = raw_config.get('encoding', 'utf-8'))
    logger.info(f'RAW validation completed. {len(list_errors)} errors/warnings found')

if __name__ == "__main__":
    raw_validator(RAW_CONFIG_PATH)