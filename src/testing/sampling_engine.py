"""
Runs the sampling loop based on which two config fields were supplied

Notes:
- sleep interval is calculated based on the configuration items that are provided
- run duration is determined by either number of samples or run time
- sleep interval takes measurement time into consideration
"""

from __future__ import annotations

import time
from typing import Dict
from src.models.ammeter_type import AmmeterType
from src.models.sampling_config import SamplingConfig
from src.testing.ammeter_api import request_measurement_from_ammeter
from src.utils.logger import get_default_logger


class SamplingEngine:
    def __init__(self, ammeter_type: AmmeterType, device_id: str, config: Dict):
        self.ammeter_type = ammeter_type
        self.device_id = device_id
        self.config = config
        self.sampling_config = SamplingConfig.from_config(config)
        self.interval_s = self._resolve_interval()
        self.log = get_default_logger(config)

    def _resolve_interval(self) -> float:
        # Derive the sample interval from whichever two fields are supplied
        c = self.sampling_config

        if c.sampling_frequency_hz is not None:
            # Pair involving frequency: frequency defines the interval
            return 1.0 / c.sampling_frequency_hz

        if c.measurements_count is not None and c.total_duration_seconds is not None:
            # count + duration: spread N samples evenly over the duration
            return c.total_duration_seconds / c.measurements_count

        raise ValueError(
            "sampling engine: cannot resolve interval from "
            f"{c.supplied_fields()}"
        )

    def run(self):
         # Execute the sampling loop, returning the list of measurements.
        c = self.sampling_config
        self.log.info("Sampling started: %s (interval %.4fs)",c.summary(), self.interval_s,)
        start = time.monotonic()
        samples = []
        n = 0

        while True:
            # Stop conditions
            if c.measurements_count is not None and n >= c.measurements_count:
                break
            if c.total_duration_seconds is not None and time.monotonic() - start >= c.total_duration_seconds:
                break

            # get measurement
            samples.append(request_measurement_from_ammeter(self.ammeter_type, self.device_id, self.config))
            n += 1

            # Absolute-time scheduling: sleep until the next scheduled
            # instant, not for a fixed interval. Prevents drift.
            next_target = start + n * self.interval_s
            sleep_for = next_target - time.monotonic()
            if sleep_for > 0:
                time.sleep(sleep_for)

        elapsed = time.monotonic() - start
        self.log.info("Sampling finished: %d samples in %.3fs",n, elapsed)
        return samples, elapsed
