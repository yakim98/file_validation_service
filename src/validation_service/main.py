from .config_paths import (RAW_CONFIG_PATH,
                           RAW_DATA_PATH,
                           RAW_VALIDATION_REPORT_FILE_PATH,
                           )
from .raw_validator import raw_validator
from .file_utils import load_yaml_config
import sys


def main():
    mode = sys.argv[1].lower()
    if mode == "raw":
        raw_config = load_yaml_config(RAW_CONFIG_PATH)
        raw_validator(raw_config=raw_config,
                      base_path=RAW_DATA_PATH,
                      report_path=RAW_VALIDATION_REPORT_FILE_PATH
                      )
    else:
        raise ValueError(f'Unknow validation mode: {mode}')

if __name__ == "__main__":
    main()
