"""
Test Framework loads config and runs the tests

Notes:
- Most configuration is fetched from the config file
- emulators are configured based on what is listed in the config
- config is passed around and can easily be mocked for testing
- config file can easily be modified by CI by dumping inside the docker
"""


import time
from typing import Dict

from src.models.ammeter_type import AmmeterType
from src.models.sampling_config import SamplingConfig
from src.models.test_result import TestResult
from src.testing.sampling_engine import SamplingEngine
from src.utils.config import load_config, get_test_name, get_ammeters, get_ammeter_settings
from src.testing.ammeter_api import setup_emulators
from src.utils.logger import TestLogger, get_default_logger
from src.utils.reporter import save_report


class AmmeterTestFramework:
    def __init__(self, config_path: str = "../../config/config.yaml"):
        self.config = load_config(config_path)
        self.log = TestLogger(self.config)
        setup_emulators(self.config)
        time.sleep(3)

    def run_test(self, config: Dict) :
        log = get_default_logger(config)
        log.info(f"Running test: {get_test_name(config)}")
        sampling_config = SamplingConfig.from_config(config)
        log.info(f"Sampling config: {sampling_config}")

        for ammeter in get_ammeters(config).keys():
            log.info(f"Sampling ammeter: {ammeter}")
            ammeter_type = AmmeterType(ammeter)
            device_id = get_ammeter_settings(config, ammeter_type, "device_id")
            try:
                # get measurements
                engine = SamplingEngine(ammeter_type, device_id, config)
                samples = engine.run()
                log.info(f"    -> {len(samples)} samples collected\n")

                # save results
                result = TestResult(ammeter_type, device_id, sampling_config, samples)
                log.info(f"\n{result.summary()}\n")

                # Archive results
                save_report(result, config)
            except ValueError as e:
                log.error(f"    ERROR -> {e}\n")


if __name__ == "__main__":

        test = AmmeterTestFramework()
        test.run_test(test.config)

