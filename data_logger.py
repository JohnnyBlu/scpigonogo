# data_logger.py
# Version: 0.2.0

import csv
import datetime
from common import TrialResult, TestConfig

class DataLogger:
    def __init__(self, config: TestConfig):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{config.lot_number}_{timestamp}.csv"
        self.csvfile = open(self.filename, mode='w', newline='')
        self._write_header(config)
        self.writer = self._get_writer()
        print(f"Logging to {self.filename}")

    def _write_header(self, config: TestConfig):
        self.csvfile.write(f"# Lot Name: {config.lot_name}\n")
        self.csvfile.write(f"# Lot Number: {config.lot_number}\n")
        self.csvfile.write(f"# Estimated Mean (A): {config.est_mean}\n")
        self.csvfile.write(f"# Estimated Std Dev: {config.est_std}\n")
        self.csvfile.write(f"# Test Duration (seconds): {config.stimulus_duration}\n")
        self.csvfile.write(f"# PSU: {config.psu_id}\n")
        self.csvfile.write(f"# DMM: {config.dmm_id}\n")
        self.csvfile.write(f"# Scope: {config.scope_id or 'Unknown'}\n")
        self.csvfile.write(f"# Test Start Time: {datetime.datetime.now()}\n")

    def _get_writer(self):
        fieldnames = [
            "lot_number", "lot_name", "trial", "stimulus_level", "resistance_ohm",
            "voltage_5p_V", "voltage_20p_V", "voltage_50p_V", "voltage_90p_V",
            "go"
        ]
        writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
        writer.writeheader()
        return writer

    def log_trial(self, result: TrialResult):
        self.writer.writerow(result.to_dict())
        self.csvfile.flush()

    def close(self):
        self.csvfile.close()
        print(f"Log file {self.filename} closed.")

    def get_filename(self):
        return self.filename
