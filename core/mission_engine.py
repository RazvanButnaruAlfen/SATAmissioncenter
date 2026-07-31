from datetime import date, datetime
from zoneinfo import ZoneInfo
import streamlit as st

from core.date_logic import ROMANIA_ARRIVAL, PLOIESTI_ARRIVAL, BRASOV_START, BRASOV_END
from core.distance import interpolate_distance
from core.mission_state import MissionState

START_DATE = date(2026, 7, 31)
START_DISTANCE_KM = 1984

def _today_in_romania() -> date:
    return datetime.now(ZoneInfo("Europe/Bucharest")).date()

def get_mission_state() -> MissionState:
    with st.sidebar:
        st.subheader("Development controls")
        test_mode = st.toggle("Mod testare dată", value=True)
        current_date = (
            st.date_input("Data simulată", value=_today_in_romania())
            if test_mode else _today_in_romania()
        )

    if current_date < ROMANIA_ARRIVAL:
        total = max(1, (ROMANIA_ARRIVAL - START_DATE).days)
        elapsed = max(0, (current_date - START_DATE).days)
        progress = min(45, round(elapsed / total * 45))
        return MissionState(current_date, "Europa", "europe", "plane",
                            "Amersfoort", "România",
                            interpolate_distance(START_DISTANCE_KM, progress),
                            progress, max(0, (ROMANIA_ARRIVAL-current_date).days))

    if current_date < PLOIESTI_ARRIVAL:
        total = max(1, (PLOIESTI_ARRIVAL - ROMANIA_ARRIVAL).days)
        elapsed = max(0, (current_date - ROMANIA_ARRIVAL).days)
        progress = 45 + round(elapsed / total * 40)
        return MissionState(current_date, "România", "romania", "car",
                            "România", "Ploiești",
                            max(0, 423 - round(elapsed / total * 423)),
                            min(85, progress), max(0, (PLOIESTI_ARRIVAL-current_date).days))

    if current_date < BRASOV_START:
        return MissionState(current_date, "Ploiești", "romania", "car",
                            "Ploiești", "Brașov", 110, 88,
                            max(0, (BRASOV_START-current_date).days))

    if current_date <= BRASOV_END:
        return MissionState(current_date, "Brașov", "romania", "car",
                            "Brașov", "Timp împreună", 0, 100,
                            max(0, (BRASOV_END-current_date).days))

    return MissionState(current_date, "România", "romania", "car",
                        "România", "Următoarea amintire", 0, 100, 0)
