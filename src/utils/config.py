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