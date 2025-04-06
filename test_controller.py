import subprocess
import json
import time
import csv
import os
from datetime import datetime

DMM_ADDR = "SIM::DMM"
PSU_ADDR = "SIM::PSU"
GONOGO_STATE_FILE = "gonogo_state.rds"

def send_to_r(trial_data, gonogo_state_file):
    result = subprocess.run(
        ["Rscript", "gonogo_driver.R", json.dumps(trial_data), gonogo_state_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("R error:", result.stderr)
        raise RuntimeError("R gonogo_driver failed")
    return json.loads(result.stdout.strip())

def log_trial(trial, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=trial.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(trial)

def print_model_info(response):
    if "mu" in response and "sigma" in response:
        print(f"μ = {response['mu']:.4f} A | σ = {response['sigma']:.4f} A", end='')
        if "confint_mu" in response:
            ci_mu = response["confint_mu"]
            print(f" | 95% CI(μ) = [{ci_mu[0]:.4f}, {ci_mu[1]:.4f}]")
        else:
            print()
        print(f"Trials: {response.get('trials_so_far')} / {response.get('max_trials')}")
    else:
        print("Waiting for model fit...")

def main():
    print("\n🔧 Electric Match Test Initialization 🔧")
    lot = input("Enter lot number: ")
    mu_est = float(input("Estimated mean (A): "))
    sigma_est = float(input("Estimated sigma (A): "))
    duration = float(input("Stimulus ON time (s): "))

    os.makedirs("data", exist_ok=True)
    logfile = f"data/log_lot_{lot}.csv"

    print("\n✅ Beginning test loop...")
    trial_num = 1
    done = False
    last_stimulus = None

    while not done:
        print(f"\n--- Trial {trial_num} ---")
        resistance = round(0.8 + 0.7 * os.urandom(1)[0] / 255.0, 2)
        print(f"Measured resistance: {resistance} ohms")

        trial_data = {
            "trial": trial_num,
            "stimulus": last_stimulus,
            "response": None if trial_num == 1 else go_nogo,
            "resistance": resistance,
            "timestamp": datetime.now().isoformat(),
            "lot": lot,
            "mu_est": mu_est,
            "sigma_est": sigma_est
        }

        response = send_to_r(trial_data, GONOGO_STATE_FILE)
        print_model_info(response)

        if response.get("done") or response.get("stimulus") is None:
            print("✅ Converged. Ending test.")
            break

        stim = response["stimulus"]
        print(f"Apply stimulus: {stim:.4f} A for {duration}s (simulated pulse)")

        go_nogo = input("Result? GO (g) / NO-GO (n): ").strip().lower()
        while go_nogo not in ("g", "n"):
            go_nogo = input("Please enter 'g' or 'n': ").strip().lower()
        go_nogo = 1 if go_nogo == "g" else 0

        trial_data["stimulus"] = stim
        trial_data["response"] = go_nogo
        log_trial(trial_data, logfile)

        last_stimulus = stim
        trial_num += 1

if __name__ == "__main__":
    main()
