"""
Interface to ammeters

Notes:
- Handles setup of emulators
- Reads measurements

"""
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
from src.utils.logger import get_default_logger


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
    log = get_default_logger(config)
    for ammeterType, details in config.get("ammeters", {}).items():
        ammeter = AmmeterType(ammeterType) # cast to enum
        port = details.get("port", {})

        match ammeter:
            case AmmeterType.GREENLEE:
                log.debug(f"Starting Greenlee on port {port}")
                threading.Thread(target=run_greenlee_emulator, args=(port,), daemon=True).start()
            case AmmeterType.ENTES:
                log.debug(f"Starting Entes on port {port}")
                threading.Thread(target=run_entes_emulator, args=(port,), daemon=True).start()
            case AmmeterType.CIRCUTOR:
                log.debug(f"Starting Circutor on port {port}")
                threading.Thread(target=run_circutor_emulator, args=(port,), daemon=True).start()

def request_measurement_from_ammeter(ammeter_type: AmmeterType, device_id: str, config: Dict) -> Measurement | None:
    log = get_default_logger(config)
    with socket(AF_INET, SOCK_STREAM) as s:
        port = get_ammeter_settings(config, ammeter_type, "port")
        if not port:
            log.warning(f"Port not configured for {ammeter_type}")
            return None
        command = get_ammeter_settings(config, ammeter_type, "command")
        if not command:
            log.warning(f"Command not configured for {ammeter_type}")
            return None
        s.connect(('localhost', port))
        s.sendall(command.encode("utf-8"))
        data = s.recv(1024)
        if data:
            measurement = Measurement(
                value_amperes=float(data.decode('utf-8')),
                timestamp=time.monotonic(),
                wall_time=datetime.datetime.now(datetime.timezone.utc),
                device_type=ammeter_type,
                device_id=device_id,
            )
            log.debug(measurement)
            return measurement
        else:
            log.warning(f"{ammeter_type} didnt return data on port {port}, using command {command}")
            return None

