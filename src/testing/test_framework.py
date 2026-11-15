import time
from typing import Dict

from src.models.ammeter_type import AmmeterType
from src.utils.config import load_config
from src.utils.helpers import setup_emulators, request_measurement_from_ammeter


class AmmeterTestFramework:
    def __init__(self, config_path: str = "../../config/config.yaml"):
        self.config = load_config(config_path)
        setup_emulators(self.config)
        time.sleep(3)


    def run_test(self, config: Dict) :
        m = request_measurement_from_ammeter(AmmeterType.GREENLEE, "gree", config)
        m1 = request_measurement_from_ammeter(AmmeterType.ENTES, "ent", config)
        m2 = request_measurement_from_ammeter(AmmeterType.CIRCUTOR, "circ1", config)
        print(m)
        print(m1)
        print(m2)

if __name__ == "__main__":

        test = AmmeterTestFramework()
        test.run_test(test.config)

