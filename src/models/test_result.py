import statistics
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any

from src.models.ammeter_type import AmmeterType
from src.models.measurement import Measurement
from src.models.sampling_config import SamplingConfig


@dataclass
class TestResult:
    device_type: AmmeterType
    device_id: str
    config: SamplingConfig
    duration: float
    samples: list[Measurement]

    # Statistical metrics
    @property
    def values(self) -> list[float]:
        return [m.value_amperes for m in self.samples]

    @property
    def n(self) -> int:
        return len(self.samples)

    @property
    def mean_current(self) -> float:
        return statistics.fmean(self.values)

    @property
    def median_current(self) -> float:
        return statistics.median(self.values)

    @property
    def std_dev(self) -> float:
        return statistics.stdev(self.values) if self.n > 1 else 0.0

    @property
    def min_current(self) -> float:
        return min(self.values)

    @property
    def max_current(self) -> float:
        return max(self.values)

    # Timing quality metrics
    @property
    def actual_rate_hz(self) -> float:
        return self.n / self.duration if self.duration > 0 else float("inf")

    def summary(self) -> str:
        summary = {
            "Device": f"{self.device_type.value}/{self.device_id}",
            "Started at": f"{self.samples[0].wall_time}",
            "Samples": self.n,
            "Configured Rate": f"{self.config.sampling_frequency_hz} Hz",
            "Actual Rate": f"{self.actual_rate_hz:.3f} Hz",
            "Duration": f"{self.duration:.3f} s",
            "Mean Current": f"{self.mean_current:.6f} A",
            "Median Current": f"{self.median_current:.6f} A",
            "Std Dev": f"{self.std_dev:.6f} A",
            "Min Current": f"{self.min_current:.6f} A",
            "Max Current": f"{self.max_current:.6f} A",
        }
        lines = [f"{key:<18}: {value}" for key, value in summary.items()]
        return "\n".join(lines)

    # for json serialization
    def asdict(self) -> dict[str, Any]:
        return asdict(self, dict_factory=_json_dict_factory)

def _clean_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_clean_value(item) for item in value]
    return value

def _json_dict_factory(items: list[tuple[str, Any]]) -> dict[str, Any]:
    return {key: _clean_value(value) for key, value in items}


