import streamlit as st
from core.mission_state import MissionState

def render_mission_map(state: MissionState) -> None:
    vehicle = "✈️" if state.vehicle == "plane" else "🚗"
    map_title = "Harta Europei" if state.map_name == "europe" else "Harta României"
    st.markdown(
        f'''
        <div style="background:#101923;color:white;border-radius:18px;
        padding:1.5rem;margin-bottom:1rem;border:1px solid #304454;">
          <div style="font-size:.8rem;letter-spacing:.12em;color:#9eb2c1;">
            {map_title.upper()}
          </div>
          <div style="font-size:1.45rem;font-weight:800;margin-top:.4rem;">
            {state.location} → {state.next_target}
          </div>
          <div style="display:flex;align-items:center;gap:.8rem;margin-top:2rem;margin-bottom:1.2rem;">
            <div style="font-size:2.5rem;">🙂</div>
            <div style="position:relative;flex:1;height:12px;background:#344957;border-radius:8px;">
              <div style="width:{state.progress_percent}%;height:100%;
              background:linear-gradient(90deg,#28a9ff,#ff6ca8);border-radius:8px;"></div>
              <div style="position:absolute;left:calc({state.progress_percent}% - 18px);
              top:-25px;font-size:2rem;">{vehicle}</div>
            </div>
            <div style="font-size:2.5rem;">😊</div>
          </div>
          <div style="font-size:2rem;font-weight:900;">{state.distance_km} km</div>
          <div style="color:#9eb2c1;">distanță operațională estimată</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
