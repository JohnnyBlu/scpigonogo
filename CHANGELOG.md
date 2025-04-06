# CHANGELOG

## [0.1.0] - Initial Integration

### Added
- Created `common.py` for unified `TrialResult` and `TestConfig` data structures.
- Refactored:
  - `live_plot.py` to accept `TrialResult` objects.
  - `data_logger.py` to write `TrialResult` objects to CSV.
  - `gonogo_interface.py` to record results from `TrialResult`.
  - `scpi_instruments.py` to cleanly return resistance and voltage as separate values.
- Added main script `run_gonogo_test.py` to integrate all modules:
  - Collects user inputs
  - Connects instruments
  - Runs test loop
  - Tracks convergence
  - Handles cleanup
