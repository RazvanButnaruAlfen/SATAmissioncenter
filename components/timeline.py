import streamlit as st
from core.mission_state import MissionState

def render_timeline(state: MissionState) -> None:
    st.markdown("### Cronologia misiunii")
    steps = [("31 iulie","Amersfoort"),("9 august","România"),
             ("14 august","Ploiești"),("15–17 august","Brașov")]
    for col, (d, p) in zip(st.columns(4), steps):
        with col:
            st.markdown(f"**{d}**")
            st.caption(p)
