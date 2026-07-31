import streamlit as st
from core.mission_state import MissionState

def render_cards(state: MissionState) -> None:
    st.markdown("### Parametri operaționali")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faza", state.phase)
    c2.metric("Vehicul", "Avion" if state.vehicle == "plane" else "Mașină")
    c3.metric("Progres", f"{state.progress_percent}%")
    c4.metric("Zile rămase", state.days_remaining)
