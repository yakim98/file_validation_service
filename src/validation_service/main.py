from file_utils import load_yaml_config
from config_paths import RAW_CONFIG_PATH
from raw_validator import raw_validator

def main():
    config_path = RAW_CONFIG_PATH

    config = load_yaml_config(config_path)
    validator = raw_validator(config_path)

if __name__ == "__main__":
    main()

