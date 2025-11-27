from pathlib import Path
from typing import Any, Dict
import yaml
from logger import get_logger

logger = get_logger(__name__)

def load_yaml_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        logger.error(f"Config file file not found: {path}")
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r") as file:
            config = yaml.safe_load(file)
            if not isinstance(config, dict):
                raise ValueError("Config file is not a dictionary")
            return config

