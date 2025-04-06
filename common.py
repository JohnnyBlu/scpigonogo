# common.py
# Version: 0.1.0

from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class TrialResult:
    lot_number: str
    lot_name: str
    trial: int
    stimulus_level: float
    resistance_ohm: float
    voltage_5p_V: Optional[float] = None
    voltage_20p_V: Optional[float] = None
    voltage_50p_V: Optional[float] = None
    voltage_90p_V: Optional[float] = None
    go: bool = False

    def to_dict(self):
        return asdict(self)

@dataclass
class TestConfig:
    lot_number: str
    lot_name: str
    est_mean: float
    est_std: float
    stimulus_duration: float
    psu_id: str
    dmm_id: str
    scope_id: Optional[str] = None
