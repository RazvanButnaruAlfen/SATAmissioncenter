import streamlit as st
from components.header import render_header
from components.device import detect_device
from components.mission_map import render_mission_map
from components.timeline import render_timeline
from components.cards import render_cards
from components.footer import render_footer
from components.funny_panel import render_funny_panel
from components.knowledge_panel import render_knowledge_panel
from components.lab_launcher import render_lab_launcher
from components.emotion_scanner import render_emotion_scanner
from components.classified_archives import render_classified_archives
from core.mission_engine import get_mission_state

st.set_page_config(
    page_title="S.A.T.A. Mission Center — Development Build",
    page_icon="📡",
    layout="wide",
)

device = detect_device()
state = get_mission_state()
st.session_state["sata_is_mobile"] = device.is_mobile
render_header()
render_mission_map(state)
render_timeline(state)
render_cards(state)
render_funny_panel(state)
render_knowledge_panel(state)
render_emotion_scanner(state)
render_classified_archives(state)
render_lab_launcher()
render_footer()
