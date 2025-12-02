from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_CONFIG_PATH = ROOT_DIR / "src/validation_service/raw_validation_config/raw_config.yaml"

RAW_DATA_PATH = ROOT_DIR / "src/files/raw"
SOURCE_DATA_PATH = ROOT_DIR / "src/files/source"

REPORT_FOLDER_PATH = ROOT_DIR / "src/files/raw/reports"
REPORT_FILE_PATH = REPORT_FOLDER_PATH / "report_raw_validation.csv"