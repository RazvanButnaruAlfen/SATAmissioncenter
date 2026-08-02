from datetime import date, datetime
from zoneinfo import ZoneInfo
import streamlit as st

from core.date_logic import ROMANIA_ARRIVAL, PLOIESTI_ARRIVAL, BRASOV_START, BRASOV_END
from core.distance import interpolate_distance
from core.mission_state import MissionState
from core.app_config import RELEASE_MODE

START_DATE = date(2026, 7, 31)
START_DISTANCE_KM = 1984

def _today_in_romania() -> date:
    return datetime.now(ZoneInfo("Europe/Bucharest")).date()

def get_mission_state() -> MissionState:
    current_date = _today_in_romania()

    if not RELEASE_MODE:
        with st.sidebar:
            st.subheader("Development controls")
            test_mode = st.toggle("Mod testare dată", value=True)
            current_date = (
                st.date_input("Data simulată", value=current_date)
                if test_mode
                else current_date
            )

    if current_date < ROMANIA_ARRIVAL:
        # Până pe 8 august nu există deplasare fizică.
        # Se schimbă doar numărătoarea inversă; avionul și distanța rămân la origine.
        return MissionState(
            current_date=current_date,
            phase="Așteptare plecare",
            map_name="europe",
            vehicle="plane",
            location="Amersfoort",
            next_target="Zbor spre România",
            distance_km=START_DISTANCE_KM,
            progress_percent=0,
            days_remaining=max(0, (ROMANIA_ARRIVAL - current_date).days),
        )

    # 9–11 august: staționare în Cluj-Napoca.
    if date(2026, 8, 9) <= current_date <= date(2026, 8, 11):
        return MissionState(
            current_date=current_date,
            phase="Staționare Cluj-Napoca",
            map_name="romania",
            vehicle="stationary",
            location="Cluj-Napoca",
            next_target="Târgu Mureș",
            distance_km=105,
            progress_percent=45,
            days_remaining=max(0, (date(2026, 8, 12) - current_date).days),
        )

    # 12 august: deplasare Cluj-Napoca -> Târgu Mureș.
    if current_date == date(2026, 8, 12):
        return MissionState(
            current_date=current_date,
            phase="Cluj-Napoca → Târgu Mureș",
            map_name="romania",
            vehicle="car",
            location="În tranzit",
            next_target="Târgu Mureș",
            distance_km=53,
            progress_percent=58,
            days_remaining=0,
        )

    # 13 august: staționare în Târgu Mureș.
    if current_date == date(2026, 8, 13):
        return MissionState(
            current_date=current_date,
            phase="Staționare Târgu Mureș",
            map_name="romania",
            vehicle="stationary",
            location="Târgu Mureș",
            next_target="Ploiești",
            distance_km=330,
            progress_percent=72,
            days_remaining=1,
        )

    # 14 august: deplasare Târgu Mureș -> Ploiești și sosire.
    if current_date == PLOIESTI_ARRIVAL:
        return MissionState(
            current_date=current_date,
            phase="Târgu Mureș → Ploiești",
            map_name="romania",
            vehicle="car",
            location="În tranzit spre Ploiești",
            next_target="Ploiești",
            distance_km=0,
            progress_percent=88,
            days_remaining=0,
        )

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
