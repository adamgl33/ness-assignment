import logging

import yaml

from typing import Dict, Any
from src.models.ammeter_type import AmmeterType


def load_config(config_path: str) -> Dict:
    """
    טעינת קובץ הקונפיגורציה
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_ammeter_settings(config: Dict, ammeter_type: str | AmmeterType, config_param: str, default: Any = None,) -> Any:
    return config.get("ammeters", {}).get(ammeter_type, {}).get(config_param, default)

def get_logger_default_name(config: Dict) -> Any | None:
    return config.get("logger", {}).get("name")

def get_test_name(config: Dict) -> Any | None:
    return config.get("test", {}).get("name")

def get_logger_level(config: Dict) -> int:
    return get_log_level_from_string(config.get("logger", {}).get("level", {}))

def get_logger_dir(config: Dict) -> Any:
    return config.get("logger", {}).get("directory")

def get_log_level_from_string(level_name: str, default: int = logging.INFO) -> int:
    level = getattr(logging, level_name.upper(), None)
    return level if isinstance(level, int) else default