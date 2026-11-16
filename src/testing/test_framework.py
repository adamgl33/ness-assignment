import time
from typing import Dict

from src.models.ammeter_type import AmmeterType
from src.utils.config import load_config, get_test_name
from src.utils.helpers import setup_emulators, request_measurement_from_ammeter
from src.utils.logger import TestLogger, get_default_logger


class AmmeterTestFramework:
    def __init__(self, config_path: str = "../../config/config.yaml"):
        self.config = load_config(config_path)
        self.log = TestLogger(self.config)
        setup_emulators(self.config)
        time.sleep(3)


    def run_test(self, config: Dict) :
        log = get_default_logger(config)
        log.info(f"Running test: {get_test_name(config)}")
        m = request_measurement_from_ammeter(AmmeterType.GREENLEE, "gree", config)
        m1 = request_measurement_from_ammeter(AmmeterType.ENTES, "ent", config)
        m2 = request_measurement_from_ammeter(AmmeterType.CIRCUTOR, "circ1", config)
        log.info(m)
        log.info(m1)
        log.info(m2)

if __name__ == "__main__":

        test = AmmeterTestFramework()
        test.run_test(test.config)

