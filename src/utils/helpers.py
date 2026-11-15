import threading
import time
import datetime

from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from src.models.measurement import Measurement
from src.models.ammeter_type import AmmeterType
from socket import socket, AF_INET, SOCK_STREAM
from typing import Dict

from src.utils.config import get_ammeter_settings


def run_greenlee_emulator(port: int):
    greenlee = GreenleeAmmeter(port)
    greenlee.start_server()

def run_entes_emulator(port: int):
    entes = EntesAmmeter(port)
    entes.start_server()

def run_circutor_emulator(port: int):
    circutor = CircutorAmmeter(port)
    circutor.start_server()

def setup_emulators(config: Dict):
    for ammeterType, details in config["ammeters"].items():
        ammeter = AmmeterType(ammeterType) # cast to enum
        port = details["port"]

        match ammeter:
            case AmmeterType.GREENLEE:
                print(f"Starting Greenlee on port {port}")
                threading.Thread(target=run_greenlee_emulator, args=(port,), daemon=True).start()
            case AmmeterType.ENTES:
                print(f"Handling Entes on port {port}")
                threading.Thread(target=run_entes_emulator, args=(port,), daemon=True).start()
            case AmmeterType.CIRCUTOR:
                print(f"Handling Circutor on port {port}")
                threading.Thread(target=run_circutor_emulator, args=(port,), daemon=True).start()

def request_measurement_from_ammeter(ammeter_type: AmmeterType, device_id: str, config: Dict) -> Measurement | None:
    with socket(AF_INET, SOCK_STREAM) as s:
        port = get_ammeter_settings(config, ammeter_type, "port")
        command = get_ammeter_settings(config, ammeter_type, "command")
        s.connect(('localhost', port))
        s.sendall(command.encode("utf-8"))
        data = s.recv(1024)
        if data:
            return Measurement(
                value_amperes=float(data.decode('utf-8')),
                timestamp=time.monotonic(),
                wall_time=datetime.datetime.now(datetime.timezone.utc),
                device_type=ammeter_type,
                device_id=device_id,
            )
        else: return None

