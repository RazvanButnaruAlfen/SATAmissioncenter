import base64
import textwrap
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from core.mission_state import MissionState

BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR_DIR = BASE_DIR / "assets" / "avatars"

def _image_data(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")

def render_mission_map(state: MissionState) -> None:
    razvan = _image_data(AVATAR_DIR / "razvan_avatar.png")
    alexandra = _image_data(AVATAR_DIR / "alexandra_avatar.png")

    is_europe = state.map_name == "europe"
    vehicle = "✈" if state.vehicle == "plane" else "🚗"
    map_title = "PROTOCOL EUROPA" if is_europe else "PROTOCOL ROMÂNIA"
    map_label = "HARTA EUROPEI" if is_europe else "HARTA ROMÂNIEI"
    left_place = "AMERSFOORT, OLANDA" if is_europe else state.location.upper()
    right_place = "PLOIEȘTI, ROMÂNIA" if state.phase != "Brașov" else "BRAȘOV, ROMÂNIA"

    if is_europe:
        scene_progress = state.progress_percent
    else:
        scene_progress = max(8, min(100, (state.progress_percent - 45) * 100 / 55))

    html = r"""
    <style>
    @keyframes sataPulse {
        0%,100% { transform: scale(1); filter: brightness(1); }
        50% { transform: scale(1.035); filter: brightness(1.13); }
    }
    @keyframes routeGlow {
        0%,100% { box-shadow: 0 0 10px rgba(63,169,255,.35); }
        50% { box-shadow: 0 0 24px rgba(255,112,184,.55); }
    }
    @keyframes vehicleFloat {
        0%,100% { transform: translateY(0) rotate(-3deg); }
        50% { transform: translateY(-7px) rotate(3deg); }
    }
    .mission-shell {
        position:relative; overflow:hidden; border-radius:24px;
        padding:22px 32px 24px; color:white;
        background:
          radial-gradient(circle at 25% 35%, rgba(31,117,180,.18), transparent 35%),
          radial-gradient(circle at 77% 38%, rgba(214,62,137,.18), transparent 35%),
          linear-gradient(145deg,#07111b,#101e2b 58%,#09131d);
        border:1px solid #2b4354;
        box-shadow:0 18px 42px rgba(0,0,0,.18);
        margin-bottom:18px;
    }
    .mission-grid {
        position:absolute; inset:0; opacity:.16;
        background-image:
          linear-gradient(rgba(110,165,200,.18) 1px,transparent 1px),
          linear-gradient(90deg,rgba(110,165,200,.18) 1px,transparent 1px);
        background-size:38px 38px;
    }
    .mission-head { position:relative; z-index:2; text-align:center; }
    .mission-kicker { color:#62b9f2; font-weight:800; letter-spacing:.14em; font-size:.78rem; }
    .mission-title { font-size:1.65rem; font-weight:900; margin-top:4px; }
    .mission-distance { font-size:3rem; font-weight:900; color:#f49ac2; line-height:1.05; margin-top:10px; }
    .mission-distance-label { color:#a7b9c7; font-size:.84rem; letter-spacing:.08em; }
    .mission-row {
        position:relative; z-index:2; display:grid;
        grid-template-columns:190px 1fr 190px;
        align-items:center; gap:18px; margin-top:14px;
    }
    .avatar-card { text-align:center; }
    .avatar-img {
        width:155px; height:155px; object-fit:cover;
        animation:sataPulse 3.2s ease-in-out infinite;
        filter:drop-shadow(0 0 20px rgba(65,170,255,.35));
    }
    .avatar-card.right .avatar-img {
        filter:drop-shadow(0 0 20px rgba(255,105,180,.38));
        animation-delay:.6s;
    }
    .avatar-name { font-size:1.35rem; font-weight:900; margin-top:4px; }
    .avatar-card.left .avatar-name { color:#56b7ff; }
    .avatar-card.right .avatar-name { color:#ff82bf; }
    .avatar-place { font-size:.75rem; color:#c4d0da; margin-top:3px; }
    .route-zone { position:relative; height:120px; display:flex; align-items:center; }
    .route-base {
        position:absolute; left:0; right:0; height:7px;
        border-radius:12px; background:#30495c;
    }
    .route-fill {
        position:absolute; left:0; width:__SCENE_PROGRESS__%; height:7px;
        border-radius:12px;
        background:linear-gradient(90deg,#30a9ff,#a66bff 55%,#ff70b8);
        animation:routeGlow 2.4s ease-in-out infinite;
    }
    .route-dots {
        position:absolute; left:0; right:0; display:flex;
        justify-content:space-between; align-items:center;
    }
    .route-dots span {
        width:13px; height:13px; border-radius:50%;
        background:#6e8495; border:2px solid #b5c6d2;
    }
    .vehicle {
        position:absolute; left:calc(__SCENE_PROGRESS__% - 25px);
        top:35px; font-size:2.75rem;
        animation:vehicleFloat 1.7s ease-in-out infinite;
        text-shadow:0 0 18px rgba(255,255,255,.55);
    }
    .mission-meta {
        position:relative; z-index:2; margin-top:18px;
        display:grid; grid-template-columns:repeat(4,1fr); gap:10px;
    }
    .mission-meta > div {
        background:rgba(5,13,20,.66); border:1px solid #294252;
        border-radius:14px; padding:12px 14px; text-align:center;
    }
    .meta-label { color:#8298a8; font-size:.68rem; letter-spacing:.1em; }
    .meta-value { font-weight:800; margin-top:3px; }
    @media(max-width:850px) {
        .mission-row { grid-template-columns:1fr; }
        .route-zone { order:3; height:110px; }
        .avatar-img { width:125px; height:125px; }
        .mission-meta { grid-template-columns:1fr 1fr; }
    }
    </style>

    <section class="mission-shell">
      <div class="mission-grid"></div>
      <div class="mission-head">
        <div class="mission-kicker">__MAP_LABEL__ • __MAP_TITLE__</div>
        <div class="mission-title">MISIUNEA: APROPIERE EMOȚIONALĂ</div>
        <div class="mission-distance">__DISTANCE__ km</div>
        <div class="mission-distance-label">DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ</div>
      </div>

      <div class="mission-row">
        <div class="avatar-card left">
          <img class="avatar-img" src="data:image/png;base64,__RAZVAN__">
          <div class="avatar-name">RĂZVAN</div>
          <div class="avatar-place">__LEFT_PLACE__</div>
        </div>

        <div class="route-zone">
          <div class="route-base"></div>
          <div class="route-fill"></div>
          <div class="route-dots">
            <span></span><span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
          </div>
          <div class="vehicle">__VEHICLE__</div>
        </div>

        <div class="avatar-card right">
          <img class="avatar-img" src="data:image/png;base64,__ALEXANDRA__">
          <div class="avatar-name">ALEXANDRA</div>
          <div class="avatar-place">__RIGHT_PLACE__</div>
        </div>
      </div>

      <div class="mission-meta">
        <div><div class="meta-label">FAZA</div><div class="meta-value">__PHASE__</div></div>
        <div><div class="meta-label">VEHICUL</div><div class="meta-value">__VEHICLE_NAME__</div></div>
        <div><div class="meta-label">URMĂTORUL PUNCT</div><div class="meta-value">__NEXT_TARGET__</div></div>
        <div><div class="meta-label">PROGRES TOTAL</div><div class="meta-value">__TOTAL_PROGRESS__%</div></div>
      </div>
    </section>
    """

    replacements = {
        "__SCENE_PROGRESS__": f"{scene_progress:.1f}",
        "__MAP_LABEL__": map_label,
        "__MAP_TITLE__": map_title,
        "__DISTANCE__": str(state.distance_km),
        "__RAZVAN__": razvan,
        "__ALEXANDRA__": alexandra,
        "__LEFT_PLACE__": left_place,
        "__RIGHT_PLACE__": right_place,
        "__VEHICLE__": vehicle,
        "__PHASE__": state.phase,
        "__VEHICLE_NAME__": "Avion" if is_europe else "Mașină",
        "__NEXT_TARGET__": state.next_target,
        "__TOTAL_PROGRESS__": str(state.progress_percent),
    }
    for key, value in replacements.items():
        html = html.replace(key, value)

    components.html(
        textwrap.dedent(html).strip(),
        height=980,
        scrolling=False,
    )
