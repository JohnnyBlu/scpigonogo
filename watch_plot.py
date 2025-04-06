import pandas as pd
import matplotlib.pyplot as plt
import argparse
import time
import os

def plot_log(csv_path, mu_est=None, sigma_est=None):
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))
    while True:
        try:
            if not os.path.exists(csv_path):
                time.sleep(1)
                continue
            df = pd.read_csv(csv_path, comment="#")
            if "stimulus" not in df.columns or "response" not in df.columns:
                time.sleep(1)
                continue
            df = df.dropna(subset=["stimulus", "response"])
            go = df[df["response"] == 1]
            nogo = df[df["response"] == 0]

            ax.clear()
            ax.set_title("Go/No-Go Trials")
            ax.set_xlabel("Trial")
            ax.set_ylabel("Current (A)")
            ax.grid(True)
            ax.scatter(go["trial"], go["stimulus"], marker='o', edgecolors='green', facecolors='none', label="Go")
            ax.scatter(nogo["trial"], nogo["stimulus"], marker='x', color='red', label="No-Go")

            if mu_est:
                ax.axhline(mu_est, color="blue", linestyle="--", label="μ estimate")
            if mu_est and sigma_est:
                ax.axhline(mu_est + 3 * sigma_est, color="gray", linestyle=":", label="μ ± 3σ")
                ax.axhline(mu_est - 3 * sigma_est, color="gray", linestyle=":")

            ax.legend()
            plt.pause(2.0)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, help="Path to CSV log file")
    parser.add_argument("--mu", type=float, help="Estimated mu")
    parser.add_argument("--sigma", type=float, help="Estimated sigma")
    args = parser.parse_args()
    plot_log(args.log, args.mu, args.sigma)
