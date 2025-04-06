# live_plot.py
# Version: 0.2.0

import matplotlib.pyplot as plt
from common import TrialResult

class LivePlot:
    def __init__(self, lot_number, lot_name):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.lot_number = lot_number
        self.lot_name = lot_name

    def update(self, trial_data):
        """
        trial_data: list of TrialResult
        """
        self.ax.clear()

        for result in trial_data:
            color = 'green' if result.go else 'red'
            marker = 'o' if result.go else 'x'
            label = 'Go' if result.go else 'No-Go'
            self.ax.scatter(result.trial, result.stimulus_level, color=color, s=100, marker=marker, label=label)

        self.ax.set_title(f"Live Plot - Lot {self.lot_number}: {self.lot_name}")
        self.ax.set_xlabel("Trial Number")
        self.ax.set_ylabel("Stimulus Level (A)")
        self.ax.grid(True)

        # Deduplicate legend
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys())

        self.fig.canvas.draw()
        plt.pause(0.01)

    def close(self):
        plt.ioff()
        plt.show()
