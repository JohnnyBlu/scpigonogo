# SCPI Gonogo System

**Version: 0.1.0**

This project performs adaptive sensitivity testing of electric matches using:
- Python for instrument control, user interaction, data logging, and plotting
- R (via `rpy2`) for statistical test logic using the `gonogo.R` package

---

## 🧩 Components

- `run_gonogo_test.py` — Main runner tying all components together
- `common.py` — Shared data structures (`TrialResult`, `TestConfig`)
- `gonogo_interface.py` — Wrapper around R `gonogo()` via `rpy2`
- `scpi_instruments.py` — SCPI control for PSU and DMM
- `data_logger.py` — Logs trial data to CSV
- `live_plot.py` — Real-time stimulus vs. trial plotting
- `gonogo.R` — Statistical test engine (sourced into R)

---

## ▶️ Running the System

```bash
python3 run_gonogo_test.py
```

You will be prompted for:
- Lot info
- Estimated mean and standard deviation
- Stimulus duration
- SCPI instrument addresses
- Go/No-Go results

---

## ⚙️ Requirements

### Python packages (see `requirements.txt`):
- `rpy2`
- `matplotlib`
- `pyvisa`

Install via:
```bash
pip install -r requirements.txt
```

### R packages (must be available in your R environment):
- `MASS`
- `graphics`, `stats` (usually base packages)

Ensure `gonogo.R` is present and updated:
```R
source("gonogo.R")
```

---

## 🗃️ Output

- CSV file with trial metadata and measurements
- Live plot (opens during testing)
- Final convergence info from gonogo model

---

## 📜 Changelog

See `CHANGELOG.md` for update history.
