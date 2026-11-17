import statistics
from dataclasses import dataclass

from src.models.ammeter_type import AmmeterType
from src.models.measurement import Measurement
from src.models.sampling_config import SamplingConfig


@dataclass
class TestResult:
    device_type: AmmeterType
    device_id: str
    config: SamplingConfig
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
        span = self.samples[-1].timestamp - self.samples[0].timestamp
        return (self.n - 1) / span if span > 0 else float("inf")

    @property
    def duration_s(self) -> float:
        return self.samples[-1].timestamp - self.samples[0].timestamp

    def summary(self) -> str:
        summary = {
            "Device": f"{self.device_type.value}/{self.device_id}",
            "Started at": f"{self.samples[0].wall_time}",
            "Samples": self.n,
            "Configured Rate": f"{self.config.sampling_frequency_hz} Hz",
            "Actual Rate": f"{self.actual_rate_hz:.3f} Hz",
            "Duration": f"{self.duration_s:.3f} s",
            "Mean Current": f"{self.mean_current:.6f} A",
            "Median Current": f"{self.median_current:.6f} A",
            "Std Dev": f"{self.std_dev:.6f} A",
            "Min Current": f"{self.min_current:.6f} A",
            "Max Current": f"{self.max_current:.6f} A",
        }
        lines = [f"{key:<18}: {value}" for key, value in summary.items()]
        return "\n".join(lines)