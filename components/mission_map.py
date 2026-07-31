import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from core.mission_state import MissionState


BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR_DIR = BASE_DIR / "assets" / "avatars"
MAP_DIR = BASE_DIR / "assets" / "maps"


def _data_uri(path: Path, mime: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_mission_map(state: MissionState) -> None:
    razvan = _data_uri(AVATAR_DIR / "razvan_avatar.png", "image/png")
    alexandra = _data_uri(AVATAR_DIR / "alexandra_avatar.png", "image/png")

    # Three visual stages:
    # 1) Europe before 9 August
    # 2) Romania between 9 and 13 August
    # 3) Prahova–Brașov zoom from 14 August onward
    if state.current_date.day < 9 and state.current_date.month == 8 or state.current_date.month < 8:
        map_file = "europe.svg"
        map_title = "HARTA EUROPEI"
        protocol = "PROTOCOL EUROPA"
        vehicle = "✈"
        vehicle_name = "Avion"
        left_place = "AMERSFOORT, OLANDA"
        right_place = "PLOIEȘTI, ROMÂNIA"
        scene_progress = max(4, min(96, state.progress_percent))
    elif state.current_date.month == 8 and state.current_date.day < 14:
        map_file = "romania.svg"
        map_title = "HARTA ROMÂNIEI"
        protocol = "PROTOCOL ROMÂNIA"
        vehicle = "🚗"
        vehicle_name = "Mașină"
        left_place = "CLUJ-NAPOCA"
        right_place = "PLOIEȘTI"
        scene_progress = max(8, min(92, (state.progress_percent - 45) * 100 / 40))
    else:
        map_file = "prahova_brasov.svg"
        map_title = "ZOOM PRAHOVA – BRAȘOV"
        protocol = "PROTOCOL CONTACT"
        vehicle = "🚗"
        vehicle_name = "Mașină"
        left_place = "PLOIEȘTI"
        right_place = "BRAȘOV"
        scene_progress = max(8, min(100, 25 if state.phase == "Ploiești" else 100))

    map_uri = _data_uri(MAP_DIR / map_file, "image/svg+xml")

    html = r"""
    <style>
    html,body{margin:0;background:transparent;font-family:Arial,sans-serif;}
    @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}
    @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
    .shell{
      position:relative;overflow:hidden;border-radius:24px;padding:22px 30px 26px;color:#fff;
      background:linear-gradient(145deg,#07111b,#101e2b 60%,#09131d);
      border:1px solid #2b4354;min-height:690px;
    }
    .map-bg{
      position:absolute;left:205px;right:205px;top:120px;bottom:120px;
      background-image:url('__MAP_URI__');background-size:contain;background-position:center;background-repeat:no-repeat;
      opacity:.82;filter:drop-shadow(0 0 18px rgba(43,125,180,.25));
    }
    .head{position:relative;z-index:3;text-align:center}
    .kicker{color:#62b9f2;font-weight:800;letter-spacing:.14em;font-size:13px}
    .title{font-size:28px;font-weight:900;margin-top:4px}
    .distance{font-size:54px;font-weight:900;color:#f49ac2;margin-top:8px}
    .distance-label{color:#a7b9c7;font-size:13px;letter-spacing:.08em}
    .mission-row{
      position:relative;z-index:4;display:grid;grid-template-columns:190px 1fr 190px;
      align-items:center;gap:0;margin-top:34px;min-height:330px;
    }
    .avatar-card{text-align:center;z-index:5}
    .avatar-img{width:150px;height:150px;object-fit:cover;animation:pulse 3.2s ease-in-out infinite}
    .avatar-name{font-size:23px;font-weight:900;margin-top:5px}
    .left .avatar-name{color:#56b7ff}.right .avatar-name{color:#ff82bf}
    .place{font-size:12px;color:#c4d0da;margin-top:4px}
    .route-track{position:absolute;left:95px;right:95px;top:104px;height:80px;z-index:4}
    .route-base{position:absolute;left:0;right:0;top:0;height:7px;border-radius:12px;background:#30495c}
    .route-fill{position:absolute;left:0;top:0;width:__SCENE_PROGRESS__%;height:7px;border-radius:12px;
      background:linear-gradient(90deg,#30a9ff,#a66bff 55%,#ff70b8)}
    .dots{position:absolute;left:0;right:0;top:-4px;display:flex;justify-content:space-between}
    .dots span{width:13px;height:13px;border-radius:50%;background:#6e8495;border:2px solid #b5c6d2}
    .vehicle{position:absolute;left:calc(__SCENE_PROGRESS__% - 25px);top:-42px;font-size:44px;
      animation:float 1.7s ease-in-out infinite;text-shadow:0 0 18px rgba(255,255,255,.55)}
    .meta{position:relative;z-index:4;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:5px}
    .meta>div{background:rgba(5,13,20,.78);border:1px solid #294252;border-radius:14px;padding:12px;text-align:center}
    .label{color:#8298a8;font-size:11px;letter-spacing:.1em}.value{font-weight:800;margin-top:4px}
    </style>

    <section class="shell">
      <div class="map-bg"></div>
      <div class="head">
        <div class="kicker">__MAP_TITLE__ • __PROTOCOL__</div>
        <div class="title">MISIUNEA: APROPIERE EMOȚIONALĂ</div>
        <div class="distance">__DISTANCE__ km</div>
        <div class="distance-label">DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ</div>
      </div>

      <div class="mission-row">
        <div class="avatar-card left">
          <img class="avatar-img" src="__RAZVAN__">
          <div class="avatar-name">RĂZVAN</div>
          <div class="place">__LEFT_PLACE__</div>
        </div>

        <div class="route-track">
          <div class="route-base"></div>
          <div class="route-fill"></div>
          <div class="dots">
            <span></span><span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
          </div>
          <div class="vehicle">__VEHICLE__</div>
        </div>

        <div></div>

        <div class="avatar-card right">
          <img class="avatar-img" src="__ALEXANDRA__">
          <div class="avatar-name">ALEXANDRA</div>
          <div class="place">__RIGHT_PLACE__</div>
        </div>
      </div>

      <div class="meta">
        <div><div class="label">FAZA</div><div class="value">__PHASE__</div></div>
        <div><div class="label">VEHICUL</div><div class="value">__VEHICLE_NAME__</div></div>
        <div><div class="label">URMĂTORUL PUNCT</div><div class="value">__NEXT_TARGET__</div></div>
        <div><div class="label">PROGRES TOTAL</div><div class="value">__TOTAL_PROGRESS__%</div></div>
      </div>
    </section>
    """

    replacements = {
        "__MAP_URI__": map_uri,
        "__MAP_TITLE__": map_title,
        "__PROTOCOL__": protocol,
        "__DISTANCE__": str(state.distance_km),
        "__SCENE_PROGRESS__": f"{scene_progress:.1f}",
        "__RAZVAN__": razvan,
        "__ALEXANDRA__": alexandra,
        "__LEFT_PLACE__": left_place,
        "__RIGHT_PLACE__": right_place,
        "__VEHICLE__": vehicle,
        "__VEHICLE_NAME__": vehicle_name,
        "__PHASE__": state.phase,
        "__NEXT_TARGET__": state.next_target,
        "__TOTAL_PROGRESS__": str(state.progress_percent),
    }
    for key, value in replacements.items():
        html = html.replace(key, value)

    components.html(html, height=735, scrolling=False)
