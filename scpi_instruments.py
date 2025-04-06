# scpi_instruments.py
# Version: 0.2.0

import time
import pyvisa

class SCPIController:
    def __init__(self, psu_addr: str, dmm_addr: str):
        self.rm = pyvisa.ResourceManager()
        self.psu = self.rm.open_resource(psu_addr)
        self.dmm = self.rm.open_resource(dmm_addr)

    def query_id(self, inst, name="Instrument") -> str:
        try:
            return inst.query("*IDN?").strip()
        except Exception as e:
            print(f"Error querying {name}: {e}")
            return "Unknown"

    def reset(self, inst, name="Instrument"):
        try:
            inst.write("*RST")
            print(f"{name} reset.")
        except Exception as e:
            print(f"Reset failed for {name}: {e}")

    def measure_resistance(self) -> float:
        """Measure DUT resistance in ohms."""
        try:
            self.dmm.write("conf:res 10")
            response = self.dmm.query("val1?").strip()
            return float(response)
        except Exception:
            return float(input("Enter resistance manually (Ohms): "))

    def measure_voltage(self, delay: float) -> float:
        """Wait and then measure voltage across DUT."""
        time.sleep(delay)
        try:
            response = self.dmm.query("val1?").strip()
            return float(response)
        except Exception:
            return float(input(f"Enter DUT voltage manually (V) after {delay:.2f}s: "))

    def apply_stimulus(self, current: float):
        """Apply stimulus current (amps) using power supply."""
        try:
            self.psu.write("VOLT 12")
            self.psu.write(f"CURR {current}")
            self.psu.write("OUTP ON")
            print(f"Stimulus applied: {current} A")
        except Exception:
            print(f"Simulated stimulus application: {current} A")

    def shutdown_stimulus(self):
        """Turn off stimulus output."""
        try:
            self.psu.write("OUTP OFF")
            print("Stimulus shutdown complete.")
        except Exception:
            print("Simulated: Stimulus shutdown.")

    def close(self):
        self.psu.close()
        self.dmm.close()
        self.rm.close()
        print("SCPI resources closed.")
