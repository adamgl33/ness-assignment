# ness-assignment
# Ammeter Test Framework

An automated testing framework designed to validate and benchmark current measurements across different ammeter emulators.

---

## Prerequisites & Installation

* **Python:** Version 3.10 or higher
* **Dependencies:** Install the required packages using:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

Run the test suite from the project root directory:
```bash
python run_tests.py
```

### Outputs
* **Logs:** Saved to `results/logs/` (also streamed to `stdout`).
* **Reports:** Saved to `results/reports/` in `.json` format.

---

## Configuration

Test behavior is controlled via `config/config.yaml`. Default fallback values are defined in `utils/config.py`.

### 1. Sampling Parameters
Configure how measurements are captured using the following three fields:
* `measurements_count`
* `total_duration_seconds`
* `sampling_frequency_hz`

> **Note:** Specify values for **any two** of these parameters and leave the third as `null`. The sampling engine will automatically calculate the missing value.

### 2. Target Ammeters
Define which ammeter types to test under the `ammeters:` section. The framework dynamically loads and executes tests based on the devices listed in this section.

---

## Architecture & Design Decisions

* **System Under Test (SUT) Isolation:** The provided ammeter emulator code is treated strictly as the SUT and remains unmodified.
* **Sequential Execution:** Ammeters are currently tested sequentially using the single sampling profile defined in the active configuration file.
* **Dependency Injection & CI Readiness:** `AmmeterTestFramework` loads the configuration file once at startup and passes the config object down to individual components. This design allows:
  * Easy unit testing via mock config injection.
  * Support for multiple test suites by swapping YAML files.
  * Seamless CI/CD integration, allowing pipelines to dynamically inject generated config files into test containers.
* **Drift-Free Sampling:** To prevent cumulative timing drift during long test runs, measurement timestamps are calculated deterministically (`sample_number * sleep_interval`) rather than relying on relative sleep delays.
* **Logging & Reporting Separation:** 
  * **Logs (`stdout` & file):** Capture execution flow and summary statistics (mean, min, max, etc.) for immediate visibility in local runs or CI pipelines.
  * **JSON Reports:** Store only raw measurement data to keep artifacts lightweight and allow flexible post-processing or historical analysis.

---

## Changelog / Resolved Issues
* Fixed a command mismatch between `main.py`, `config.yaml`, and the expected emulator command interface so the main entry point executes properly.
