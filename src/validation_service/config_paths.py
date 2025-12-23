from pathlib import Path

CSV_SAMPLE_SIZE = 4096

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_CONFIG_PATH = ROOT_DIR / "src/validation_service/raw_validation_config/raw_config.yaml"
SOURCE_CONFIG_PATH = ROOT_DIR / "src/validation_service/source_validation_config/source_config.yaml"

RAW_DATA_PATH = ROOT_DIR / "src/files/raw"
SOURCE_DATA_PATH = ROOT_DIR / "src/files/source"

RAW_VALIDATION_REPORT_FOLDER_PATH = ROOT_DIR / "src/files/raw/reports"
RAW_VALIDATION_REPORT_FILE_PATH = RAW_VALIDATION_REPORT_FOLDER_PATH / "report_raw_validation.csv"
SOURCE_VALIDATION_REPORT_FOLDER_PATH = ROOT_DIR / "src/files/source/reports"
SOURCE_VALIDATION_REPORT_FILE_PATH = SOURCE_VALIDATION_REPORT_FOLDER_PATH / "report_source_validation.csv"