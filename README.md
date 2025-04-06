# scpigonogo

**Version 1.0.0**

`scpigonogo` is a Python + R system for conducting binary-response sensitivity testing using SCPI-controlled instruments and the Neyer test method implemented via the R `gonogo` package.

## Features

- Stimulus-response loop with R-driven adaptive test planning (Neyer method)
- Clean separation of logging and plotting
- Console-based reporting of model estimates (`μ`, `σ`, and 95% CI)
- Optional live trial plot viewer

## Structure

- `test_controller.py`: Main control loop (simulates SCPI)
- `gonogo_driver.R`: R interface for dose selection and fit updates
- `watch_plot.py`: Optional separate viewer for trial results
- `data/`: Trial log files saved here as CSV

## Requirements

- Python 3.x
- R with the `gonogo` package installed
- matplotlib, pandas (Python packages)

## Usage

Run the test controller:

```bash
python3 test_controller.py
```

(Optional) Watch the trials live:

```bash
python3 watch_plot.py --log data/log_lot_example.csv --mu 0.5 --sigma 0.1
```

---

MIT License. Built for efficient electrical match sensitivity testing.
