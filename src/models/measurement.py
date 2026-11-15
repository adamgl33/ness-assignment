from dataclasses import dataclass
from datetime import datetime
from src.models.ammeter_type import AmmeterType


@dataclass(frozen=True)
class Measurement:
    value_amperes: float
    timestamp: float         # monotonic clock seconds (for timing)
    wall_time: datetime           # real-world timestamp (for reports)
    device_type: AmmeterType
    device_id: str
    unit: str = "A"
