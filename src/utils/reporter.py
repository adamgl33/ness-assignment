import json
import os
from datetime import datetime
from typing import Dict

from src.models.test_result import TestResult
from src.utils.Utils import sanitize_filename
from src.utils.config import get_report_dir, get_report_filename
from src.utils.logger import get_default_logger


def save_report(result: TestResult, config: Dict):
    log = get_default_logger(config)

    # create report directory
    report_dir = get_report_dir(config)
    os.makedirs(report_dir, exist_ok=True)

    # configure filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = sanitize_filename(f"{timestamp}_{result.device_type}_{result.device_id}_{get_report_filename(config)}")
    report_fullpath = f"{report_dir}/{filename}.json"

    log.info(f"Archiving test results to: {report_fullpath}" )
    with open(report_fullpath, "w") as f:
        json.dump(result.asdict(), f, indent=2)