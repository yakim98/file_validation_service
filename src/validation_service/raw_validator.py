from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from config_loader import load_yaml_config
from file_utils import list_files, is_csv_file
from report_writer import write_report
from logger import get_logger

logger = get_logger(__name__)

DEFAULT_LINE_NUMBER = ""

def raw_validator(config_path: Path) -> None:
    config = load_yaml_config(config_path)
    raw_config = config.get('raw')
    base_path = Path(raw_config.get('base_path', "src/files/raw"))
    folders_config = raw_config.get('folders')
    report_folder = base_path / 'reports'
    report_file = report_folder / 'report_raw_validation.csv'

    list_errors: List[Dict[str, Any]] = []

    for folder in folders_config:
        name = folder.get('name')
        folder_path = base_path / name
        if not folder_path.exists():
            list_errors.append(
                {
                    "error_level": "error",
                    "error_text": f"Required folder {name} not found",
                    "file_name": DEFAULT_LINE_NUMBER,
                    "folder_name": str(folder_path),
                    "line_number": DEFAULT_LINE_NUMBER
                }
            )
        else:
            logger.info("Folder found:", folder_path)

            required_columns = folder.get('required_columns', [])
            #patterns = folder.get('file_patterns', ["*.csv"])
            files = list(list_files(folder_path, ["*"]))
            if not files:
                list_errors.append(
                    {
                        "error_level": "warning",
                        "error_text": f"Folder {name} doesn't contain any corresponding files",
                        "file_name": DEFAULT_LINE_NUMBER,
                        "folder_name": str(folder_path),
                        "line_number": DEFAULT_LINE_NUMBER
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
                            "line_number": DEFAULT_LINE_NUMBER
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
                            "line_number": DEFAULT_LINE_NUMBER
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
                                "line_number": DEFAULT_LINE_NUMBER
                            }
                        )

    write_report(list_errors, report_file, encoding = raw_config.get('encoding', 'utf-8'))
    logger.info(f'RAW validation completed. {len(list_errors)} errors/warnings found')

if __name__ == "__main__":
    raw_validator(Path("src/files/static/raw_config.yaml"))