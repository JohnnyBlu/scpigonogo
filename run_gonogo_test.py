# run_gonogo_test.py
# Version: 0.1.0

import time
from common import TrialResult, TestConfig
from scpi_instruments import SCPIController
from gonogo_interface import GonogoInterface
from data_logger import DataLogger
from live_plot import LivePlot

def main():
    # --- Initial User Inputs ---
    lot_name = input("Enter Lot Name: ")
    lot_number = input("Enter Lot Number: ")
    est_mean = float(input("Enter estimated mean stimulus (A): "))
    est_std = float(input("Enter estimated standard deviation: "))
    stimulus_duration = float(input("Enter stimulus duration (s): "))

    # --- Connect Instruments ---
    psu_addr = input("Enter PSU SCPI address: ")
    dmm_addr = input("Enter DMM SCPI address: ")
    scpi = SCPIController(psu_addr, dmm_addr)
    psu_id = scpi.query_id(scpi.psu, "PSU")
    dmm_id = scpi.query_id(scpi.dmm, "DMM")

    # --- Setup Config, Logger, Plot, Gonogo ---
    config = TestConfig(
        lot_name=lot_name,
        lot_number=lot_number,
        est_mean=est_mean,
        est_std=est_std,
        stimulus_duration=stimulus_duration,
        psu_id=psu_id,
        dmm_id=dmm_id
    )

    logger = DataLogger(config)
    plotter = LivePlot(lot_number, lot_name)
    gonogo = GonogoInterface(mlo=est_mean - 3*est_std, mhi=est_mean + 3*est_std, sg=est_std)
    gonogo.start_test()

    trial_history = []
    trial_number = 1
    prev_est = None

    try:
        while True:
            # --- Get Stimulus from Gonogo ---
            stimulus = gonogo.get_next_stimulus()
            if stimulus is None:
                print("No next stimulus level returned.")
                break

            print(f"Trial {trial_number}: Apply {stimulus:.2f} A for {stimulus_duration:.2f}s")

            # --- Resistance ---
            resistance = scpi.measure_resistance()

            # --- Stimulus ---
            scpi.apply_stimulus(stimulus)
            voltage = scpi.measure_voltage(stimulus_duration)
            scpi.shutdown_stimulus()

            # --- Go/No-Go ---
            response = input("Did the device fire? (y/n): ").strip().lower()
            go = response == 'y'

            # --- Record & Update ---
            result = TrialResult(
                lot_number=lot_number,
                lot_name=lot_name,
                trial=trial_number,
                stimulus_level=stimulus,
                resistance_ohm=resistance,
                voltage_50p_V=voltage,
                go=go
            )

            logger.log_trial(result)
            trial_history.append(result)
            plotter.update(trial_history)
            gonogo.record_result(result)

            # --- Check Convergence ---
            converged, current_est = gonogo.has_converged(prev_estimates=prev_est)
            prev_est = current_est
            if converged:
                print(f"Test converged at μ={current_est[0]:.2f}, σ={current_est[1]:.2f}")
                break

            trial_number += 1

    finally:
        logger.close()
        plotter.close()
        scpi.close()

if __name__ == "__main__":
    main()
