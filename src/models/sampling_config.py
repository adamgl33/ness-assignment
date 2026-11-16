"""
Notes:
- Exactly 2 of the 3 fields must be supplied (NULL/null/~/empty = not supplied).
- 1 or 3 supplied -> error.
- Simple validation done on raw calues
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from src.utils.logger import get_default_logger

# Field names as they appear in the config file
FIELD_MEASUREMENTS = "measurements_count"
FIELD_DURATION = "total_duration_seconds"
FIELD_FREQUENCY = "sampling_frequency_hz"

_FIELDS = (FIELD_MEASUREMENTS, FIELD_DURATION, FIELD_FREQUENCY)


@dataclass
class SamplingConfig:
    # Supplied values only — fields that were NULL stay None.
    measurements_count: int | None = None
    total_duration_seconds: float | None = None
    sampling_frequency_hz: float | None = None

    @classmethod
    def from_config(cls, config: Dict) -> "SamplingConfig":
        log = get_default_logger(config)
        # get values from config
        raw = config.get("testing", {}).get("sampling", {})

        # Validate that exactly 2 of 3 fields are supplied
        supplied = {name: raw[name] for name in _FIELDS if raw.get(name) is not None}

        if len(supplied) != 2:
            error_msg = (
                f"sampling config: {len(supplied)} of 3 fields supplied "
                f"({', '.join(supplied) if supplied else 'none'}) — "
                "exactly 2 are required: measurements_count, "
                "total_duration_seconds, sampling_frequency_hz"
            )
            log.error(error_msg)
            raise ValueError(error_msg)
        cfg = cls(**supplied)
        cfg._validate()
        return cfg

    def _validate(self) -> None:
        if self.measurements_count is not None and self.measurements_count < 1:
            raise ValueError("measurements_count must be >= 1")
        if self.total_duration_seconds is not None and self.total_duration_seconds <= 0:
            raise ValueError("total_duration_seconds must be > 0")
        if self.sampling_frequency_hz is not None and self.sampling_frequency_hz <= 0:
            raise ValueError("sampling_frequency_hz must be > 0")

    def supplied_fields(self) -> list[str]:
        # Names of the two fields that were supplied
        return [name for name in _FIELDS if getattr(self, name) is not None]

    def summary(self) -> str:
        parts = []
        if self.measurements_count is not None:
            parts.append(f"{self.measurements_count} measurements")
        if self.total_duration_seconds is not None:
            parts.append(f"{self.total_duration_seconds:.3f}s duration")
        if self.sampling_frequency_hz is not None:
            parts.append(f"{self.sampling_frequency_hz:.3f} Hz")
        return ", ".join(parts)