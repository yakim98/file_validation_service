from pathlib import Path
from config_loader import load_yaml_config
from logger import get_logger
from raw_validator import raw_validator

def main():
    config_path = Path("src/files/static/raw_config.yaml")

    config = load_yaml_config(config_path)
    validator = raw_validator(config_path)

if __name__ == "__main__":
    main()

