from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class MissionState:
    current_date: date
    phase: str
    map_name: str
    vehicle: str
    location: str
    next_target: str
    distance_km: int
    progress_percent: int
    days_remaining: int
