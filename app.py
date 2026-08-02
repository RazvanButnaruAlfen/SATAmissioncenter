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
from components.system_status import render_system_status
from components.sata_events import render_sata_events
from core.mission_engine import get_mission_state
from core.app_config import APP_ICON, APP_TITLE, RELEASE_MODE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

if RELEASE_MODE:
    st.markdown(
        """
        <style>
        /* Release shell: remove Streamlit's page navigation and sidebar. */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        button[kind="headerNoPadding"] {
            display: none !important;
        }

        /* Remove the empty space left by the hidden sidebar. */
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 0 !important;
        }

        /* Keep the release centered and visually clean. */
        .block-container {
            max-width: 1280px;
            padding-top: 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
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
render_sata_events(state.current_date)
render_emotion_scanner(state)
render_system_status()
render_classified_archives(state)
render_lab_launcher()
render_footer()
