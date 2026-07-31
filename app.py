import streamlit as st
from components.header import render_header
from components.mission_map import render_mission_map
from components.timeline import render_timeline
from components.cards import render_cards
from components.footer import render_footer
from components.funny_panel import render_funny_panel
from core.mission_engine import get_mission_state

st.set_page_config(
    page_title="S.A.T.A. Mission Center — Development Build",
    page_icon="📡",
    layout="wide",
)

state = get_mission_state()
render_header()
render_mission_map(state)
render_timeline(state)
render_cards(state)
render_funny_panel(state)
render_footer()
