from __future__ import annotations

from datetime import date
import base64
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from core.mission_state import MissionState


BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR_DIR = BASE_DIR / "assets" / "avatars"

LOCATIONS = {
    "amersfoort": (52.1561, 5.3878),
    "cluj": (46.7712, 23.6236),
    "targu_mures": (46.5425, 24.5575),
    "ploiesti": (44.9367, 26.0129),
    "brasov": (45.6427, 25.5887),
}


def _image_data(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _interpolate(start: tuple[float, float], end: tuple[float, float], progress: float):
    progress = max(0.0, min(1.0, progress))
    lat = start[0] + (end[0] - start[0]) * progress
    lon = start[1] + (end[1] - start[1]) * progress
    return lat, lon


def _stage(state: MissionState):
    current = state.current_date

    if current.month < 8 or (current.month == 8 and current.day < 9):
        start = LOCATIONS["amersfoort"]
        end = LOCATIONS["ploiesti"]
        progress = max(0.0, min(1.0, state.progress_percent / 45))
        return {
            "title": "PROTOCOL EUROPA",
            "subtitle": "Amersfoort → Ploiești",
            "start": start,
            "end": end,
            "vehicle": "✈",
            "vehicle_name": "Avion",
            "progress": progress,
            "lat_range": [41, 57],
            "lon_range": [-2, 31],
            "labels": [("Amersfoort", start), ("Ploiești", end)],
        }

    if current.month == 8 and 9 <= current.day <= 11:
        point = LOCATIONS["cluj"]
        return {
            "title": "PROTOCOL CLUJ",
            "subtitle": "Staționare în Cluj-Napoca",
            "start": point,
            "end": point,
            "vehicle": "●",
            "vehicle_name": "Staționare",
            "progress": 0.0,
            "lat_range": [45.8, 47.4],
            "lon_range": [22.6, 24.7],
            "labels": [("Cluj-Napoca", point)],
        }

    if current.month == 8 and current.day == 12:
        start = LOCATIONS["cluj"]
        end = LOCATIONS["targu_mures"]
        return {
            "title": "PROTOCOL CLUJ–TÂRGU MUREȘ",
            "subtitle": "Cluj-Napoca → Târgu Mureș",
            "start": start,
            "end": end,
            "vehicle": "🚗",
            "vehicle_name": "Mașină",
            "progress": 0.50,
            "lat_range": [45.8, 47.3],
            "lon_range": [22.7, 25.2],
            "labels": [("Cluj-Napoca", start), ("Târgu Mureș", end)],
        }

    if current.month == 8 and current.day == 13:
        point = LOCATIONS["targu_mures"]
        return {
            "title": "PROTOCOL TÂRGU MUREȘ",
            "subtitle": "Staționare în Târgu Mureș",
            "start": point,
            "end": point,
            "vehicle": "●",
            "vehicle_name": "Staționare",
            "progress": 0.0,
            "lat_range": [45.7, 47.2],
            "lon_range": [23.6, 25.6],
            "labels": [("Târgu Mureș", point)],
        }

    if current.month == 8 and current.day == 14:
        start = LOCATIONS["targu_mures"]
        end = LOCATIONS["ploiesti"]
        return {
            "title": "PROTOCOL TÂRGU MUREȘ–PLOIEȘTI",
            "subtitle": "Târgu Mureș → Ploiești",
            "start": start,
            "end": end,
            "vehicle": "🚗",
            "vehicle_name": "Mașină",
            "progress": 1.0,
            "lat_range": [44.3, 47.1],
            "lon_range": [23.4, 26.8],
            "labels": [("Târgu Mureș", start), ("Ploiești", end)],
        }

    start = LOCATIONS["ploiesti"]
    end = LOCATIONS["brasov"]
    progress = 0.18 if state.phase == "Ploiești" else 1.0
    return {
        "title": "PROTOCOL PRAHOVA–BRAȘOV",
        "subtitle": "Ploiești → Brașov",
        "start": start,
        "end": end,
        "vehicle": "🚗",
        "vehicle_name": "Mașină",
        "progress": progress,
        "lat_range": [44.45, 46.05],
        "lon_range": [24.65, 26.65],
        "labels": [("Ploiești", start), ("Brașov", end)],
    }


def _render_mobile_romania_stage(
    state: MissionState,
    stage: dict,
) -> None:
    """Compact mobile layout for all Romania stages."""
    razvan_uri = _image_data(AVATAR_DIR / "razvan_avatar.png")
    alexandra_uri = _image_data(AVATAR_DIR / "alexandra_avatar.png")

    start = stage["start"]
    end = stage["end"]
    is_stationary = start == end
    vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

    current_day = state.current_date.day

    if state.current_date.month == 8 and current_day <= 11:
        headline = "STAȚIONARE ÎN CLUJ-NAPOCA"
        distance_value = "105 km"
        distance_caption = "PÂNĂ LA URMĂTOAREA ETAPĂ"
        route_status = "Răzvan rămâne în Cluj-Napoca"
    elif state.current_date.month == 8 and current_day == 12:
        headline = "CLUJ-NAPOCA → TÂRGU MUREȘ"
        distance_value = f"{state.distance_km} km"
        distance_caption = "DISTANȚĂ RUTIERĂ ESTIMATĂ"
        route_status = "Deplasare activă"
    elif state.current_date.month == 8 and current_day == 13:
        headline = "STAȚIONARE ÎN TÂRGU MUREȘ"
        distance_value = "330 km"
        distance_caption = "PÂNĂ LA PLOIEȘTI"
        route_status = "Ultima oprire înainte de Ploiești"
    elif state.current_date.month == 8 and current_day == 14:
        headline = "TÂRGU MUREȘ → PLOIEȘTI"
        distance_value = "0 km"
        distance_caption = "SOSIRE ÎN PLOIEȘTI"
        route_status = "Contact în Ploiești"
    else:
        headline = "PLOIEȘTI → BRAȘOV"
        distance_value = f"{max(0, round(110 * (1 - stage['progress'])))} km"
        distance_caption = "DISTANȚĂ RUTIERĂ ESTIMATĂ"
        route_status = "Deplasare împreună"

    st.markdown(
        f"""
        <style>
        .rm-head {{
            background:#08131e;
            border:1px solid #294454;
            border-radius:16px 16px 0 0;
            padding:17px 14px 14px;
            text-align:center;
            color:white;
        }}
        .rm-protocol {{
            color:#63bdf4;
            font-size:.75rem;
            font-weight:900;
            letter-spacing:.08em;
        }}
        .rm-title {{
            font-size:clamp(1.25rem,6vw,1.75rem);
            line-height:1.12;
            font-weight:950;
            margin-top:.45rem;
            overflow-wrap:anywhere;
        }}
        .rm-distance {{
            color:#f49ac2;
            font-size:clamp(2.2rem,12vw,3.25rem);
            line-height:1;
            font-weight:950;
            margin-top:.65rem;
        }}
        .rm-caption {{
            color:#9fb1bf;
            font-size:.72rem;
            letter-spacing:.06em;
            margin-top:.3rem;
        }}
        .rm-status {{
            color:#ffd98d;
            font-size:.82rem;
            font-weight:800;
            margin-top:.75rem;
        }}
        .rm-people {{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:10px;
            margin-top:10px;
        }}
        .rm-person {{
            background:#0b1722;
            border:1px solid #294454;
            border-radius:14px;
            padding:10px;
            text-align:center;
            color:white;
        }}
        .rm-avatar {{
            width:72px;
            height:72px;
            object-fit:contain;
        }}
        .rm-name {{
            font-size:1rem;
            font-weight:950;
            margin-top:3px;
        }}
        .rm-person.left .rm-name {{color:#59b9ff;}}
        .rm-person.right .rm-name {{color:#ff82bf;}}
        .rm-place {{
            color:#b7c5cf;
            font-size:.72rem;
            line-height:1.25;
            margin-top:2px;
        }}
        .rm-cards {{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:10px;
            margin-top:10px;
        }}
        .rm-card {{
            background:#0b1722;
            border:1px solid #294454;
            border-radius:13px;
            padding:11px;
            min-width:0;
        }}
        .rm-label {{
            color:#8195a4;
            font-size:.68rem;
            margin-bottom:4px;
        }}
        .rm-value {{
            color:#f4f7fa;
            font-size:.92rem;
            font-weight:850;
            line-height:1.25;
            overflow-wrap:anywhere;
        }}
        </style>

        <div class="rm-head">
          <div class="rm-protocol">{stage["title"]}</div>
          <div class="rm-title">{headline}</div>
          <div class="rm-distance">{distance_value}</div>
          <div class="rm-caption">{distance_caption}</div>
          <div class="rm-status">{route_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = go.Figure()

    if is_stationary:
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0]],
                lon=[start[1]],
                mode="markers+text",
                text=[stage["labels"][0][0]],
                textposition="top right",
                textfont=dict(size=14, color="#68c2ff"),
                marker=dict(size=20, color="#36aef5"),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0]],
                lon=[start[1]],
                mode="text",
                text=["📍"],
                textfont=dict(size=28, color="#ffffff"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
    else:
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0], end[0]],
                lon=[start[1], end[1]],
                mode="lines",
                line=dict(width=6, color="#334e63"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0], vehicle_lat],
                lon=[start[1], vehicle_lon],
                mode="lines",
                line=dict(width=5, color="#36aef5"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[vehicle_lat, end[0]],
                lon=[vehicle_lon, end[1]],
                mode="lines",
                line=dict(width=4, color="#ff70b8"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0]],
                lon=[start[1]],
                mode="markers+text",
                text=[stage["labels"][0][0]],
                textposition="top left",
                textfont=dict(size=13, color="#68c2ff"),
                marker=dict(size=16, color="#36aef5"),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[end[0]],
                lon=[end[1]],
                mode="markers+text",
                text=[stage["labels"][-1][0]],
                textposition="bottom right",
                textfont=dict(size=13, color="#ff8bc5"),
                marker=dict(size=16, color="#ff70b8"),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=[vehicle_lat],
                lon=[vehicle_lon],
                mode="text",
                text=[stage["vehicle"]],
                textfont=dict(size=30, color="#ffffff"),
                hovertemplate=f"{stage['vehicle_name']}<extra></extra>",
                showlegend=False,
            )
        )

    center_lat = (stage["lat_range"][0] + stage["lat_range"][1]) / 2
    center_lon = (stage["lon_range"][0] + stage["lon_range"][1]) / 2

    if state.current_date.month == 8 and current_day <= 11:
        zoom = 6.6
    elif state.current_date.month == 8 and current_day == 12:
        zoom = 6.3
    elif state.current_date.month == 8 and current_day == 13:
        zoom = 6.6
    elif state.current_date.month == 8 and current_day == 14:
        zoom = 5.9
    else:
        zoom = 6.9

    fig.update_layout(
        height=330,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#08131e",
        plot_bgcolor="#08131e",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom,
        ),
        font=dict(family="Arial, sans-serif"),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "scrollZoom": True,
        },
    )

    if state.current_date >= date(2026, 8, 15):
        left_name = "RĂZVAN + ALEXANDRA"
        left_place = "Plecarea împreună din Ploiești"
        right_name = "DESTINAȚIE"
        right_place = "Brașov"
        right_image = alexandra_uri
    else:
        left_name = "RĂZVAN"
        left_place = state.location
        right_name = "ALEXANDRA"
        right_place = "Ploiești"
        right_image = alexandra_uri

    st.markdown(
        f"""
        <div class="rm-people">
          <div class="rm-person left">
            <img class="rm-avatar" src="{razvan_uri}">
            <div class="rm-name">{left_name}</div>
            <div class="rm-place">{left_place}</div>
          </div>
          <div class="rm-person right">
            <img class="rm-avatar" src="{right_image}">
            <div class="rm-name">{right_name}</div>
            <div class="rm-place">{right_place}</div>
          </div>
        </div>

        <div class="rm-cards">
          <div class="rm-card">
            <div class="rm-label">Faza</div>
            <div class="rm-value">{state.phase}</div>
          </div>
          <div class="rm-card">
            <div class="rm-label">Localizare</div>
            <div class="rm-value">{state.location}</div>
          </div>
          <div class="rm-card">
            <div class="rm-label">Următorul punct</div>
            <div class="rm-value">{state.next_target}</div>
          </div>
          <div class="rm-card">
            <div class="rm-label">Zile rămase</div>
            <div class="rm-value">{state.days_remaining}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mission_map(
    state: MissionState,
    is_mobile: bool | None = None,
) -> None:
    if is_mobile is None:
        is_mobile = bool(st.session_state.get("sata_is_mobile", False))

    stage = _stage(state)

    if is_mobile and state.current_date >= date(2026, 8, 9):
        _render_mobile_romania_stage(state, stage)
        return

    # Responsive Europe layout: the title and avatars are outside Plotly,
    # so they can reflow cleanly on phones without clipping.
    if is_mobile and state.current_date < date(2026, 8, 9):
        start = stage["start"]
        end = stage["end"]
        vehicle_lat, vehicle_lon = start

        razvan_uri = _image_data(AVATAR_DIR / "razvan_avatar.png")
        alexandra_uri = _image_data(AVATAR_DIR / "alexandra_avatar.png")

        st.markdown(
            f"""
            <style>
            .eu-shell {{
                background:#08131e;
                border:1px solid #294454;
                border-radius:18px 18px 0 0;
                padding:20px 22px 16px;
                text-align:center;
                color:white;
            }}
            .eu-protocol {{
                color:#63bdf4;
                font-size:clamp(.78rem,2.8vw,.95rem);
                font-weight:900;
                letter-spacing:.10em;
            }}
            .eu-title {{
                font-size:clamp(1.45rem,5.4vw,2.35rem);
                line-height:1.08;
                font-weight:950;
                margin-top:.5rem;
                overflow-wrap:anywhere;
            }}
            .eu-distance {{
                color:#f49ac2;
                font-size:clamp(2.6rem,10vw,4rem);
                line-height:1;
                font-weight:950;
                margin-top:.75rem;
            }}
            .eu-caption {{
                color:#9fb1bf;
                font-size:clamp(.72rem,2.8vw,.9rem);
                letter-spacing:.06em;
                margin-top:.35rem;
            }}
            .eu-countdown {{
                margin-top:.8rem;
                color:#ffd98d;
                font-size:clamp(.82rem,3vw,1rem);
                font-weight:800;
            }}
            .eu-avatars {{
                display:grid;
                grid-template-columns:repeat(2,minmax(0,1fr));
                gap:12px;
                margin-top:12px;
            }}
            .eu-person {{
                background:#0b1722;
                border:1px solid #294454;
                border-radius:15px;
                padding:12px;
                text-align:center;
                min-width:0;
            }}
            .eu-avatar {{
                width:clamp(76px,18vw,118px);
                height:clamp(76px,18vw,118px);
                object-fit:contain;
            }}
            .eu-name {{
                font-size:clamp(1rem,4vw,1.35rem);
                font-weight:950;
                margin-top:5px;
            }}
            .eu-person.left .eu-name {{color:#59b9ff;}}
            .eu-person.right .eu-name {{color:#ff82bf;}}
            .eu-place {{
                color:#b7c5cf;
                font-size:clamp(.72rem,2.8vw,.88rem);
                margin-top:3px;
                overflow-wrap:anywhere;
            }}
            @media(max-width:420px) {{
                .eu-shell {{padding:17px 12px 13px;}}
                .eu-avatars {{grid-template-columns:1fr;}}
                .eu-person {{
                    display:grid;
                    grid-template-columns:82px 1fr;
                    text-align:left;
                    align-items:center;
                    column-gap:12px;
                }}
                .eu-avatar {{width:78px;height:78px;grid-row:1 / span 2;}}
                .eu-name {{margin-top:0;}}
            }}
            </style>

            <div class="eu-shell">
              <div class="eu-protocol">{stage["title"]}</div>
              <div class="eu-title">MISIUNEA: APROPIERE EMOȚIONALĂ</div>
              <div class="eu-distance">{state.distance_km} km</div>
              <div class="eu-caption">DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ</div>
              <div class="eu-countdown">
                ZBORUL NU A ÎNCEPUT • {state.days_remaining} ZILE PÂNĂ LA ROMÂNIA
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = go.Figure()

        # Static route before the actual flight.
        fig.add_trace(
            go.Scattergeo(
                lat=[start[0], end[0]],
                lon=[start[1], end[1]],
                mode="lines",
                line=dict(width=4, color="#ff70b8", dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # Separate city markers avoid text-position issues.
        fig.add_trace(
            go.Scattergeo(
                lat=[start[0]],
                lon=[start[1]],
                mode="markers+text",
                text=["Amersfoort"],
                textposition="top left",
                textfont=dict(size=14, color="#68c2ff"),
                marker=dict(size=15, color="#35aef5", line=dict(width=3, color="#eef8ff")),
                hovertemplate="Amersfoort<extra></extra>",
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scattergeo(
                lat=[end[0]],
                lon=[end[1]],
                mode="markers+text",
                text=["Ploiești"],
                textposition="bottom right",
                textfont=dict(size=14, color="#ff8bc5"),
                marker=dict(size=15, color="#ff70b8", line=dict(width=3, color="#eef8ff")),
                hovertemplate="Ploiești<extra></extra>",
                showlegend=False,
            )
        )

        # Plane stays at Amersfoort until 9 August.
        fig.add_trace(
            go.Scattergeo(
                lat=[vehicle_lat],
                lon=[vehicle_lon],
                mode="text",
                text=["✈"],
                textfont=dict(size=32, color="#ffffff"),
                hovertemplate="Zborul nu a început<extra></extra>",
                showlegend=False,
            )
        )

        fig.update_geos(
            projection_type="mercator",
            showland=True,
            landcolor="#0d2233",
            showocean=True,
            oceancolor="#07131e",
            showlakes=True,
            lakecolor="#07131e",
            showcountries=True,
            countrycolor="#34749d",
            countrywidth=1.0,
            showcoastlines=True,
            coastlinecolor="#34749d",
            coastlinewidth=1.1,
            showframe=False,
            bgcolor="rgba(0,0,0,0)",
            lataxis_range=[41, 57],
            lonaxis_range=[-2, 31],
            resolution=50,
        )

        fig.update_layout(
            height=360,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#08131e",
            plot_bgcolor="#08131e",
            font=dict(family="Arial, sans-serif"),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": False,
            },
        )

        st.markdown(
            f"""
            <div class="eu-avatars">
              <div class="eu-person left">
                <img class="eu-avatar" src="{razvan_uri}">
                <div class="eu-name">RĂZVAN</div>
                <div class="eu-place">Amersfoort, Olanda</div>
              </div>
              <div class="eu-person right">
                <img class="eu-avatar" src="{alexandra_uri}">
                <div class="eu-name">ALEXANDRA</div>
                <div class="eu-place">Ploiești, România</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        c1.metric("Stare", "Așteptare plecare")
        c2.metric("Următorul eveniment", f"România în {state.days_remaining} zile")
        return

    # Detailed itinerary in Romania: Cluj, Târgu Mureș, then Ploiești.
    if state.current_date.month == 8 and 9 <= state.current_date.day <= 14:
        start = stage["start"]
        end = stage["end"]
        is_stationary = start == end
        vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

        # Distances are operational road estimates for the active or upcoming leg.
        if state.current_date.day <= 11:
            display_distance = 105
            distance_caption = "DISTANȚĂ PÂNĂ LA URMĂTOAREA ETAPĂ"
        elif state.current_date.day == 12:
            display_distance = 53
            distance_caption = "DISTANȚĂ RUTIERĂ RĂMASĂ ESTIMATĂ"
        elif state.current_date.day == 13:
            display_distance = 330
            distance_caption = "DISTANȚĂ PÂNĂ LA PLOIEȘTI"
        else:
            display_distance = 0
            distance_caption = "SOSIRE ÎN PLOIEȘTI"

        st.markdown(
            f"""
            <div style="
                background:#08131e;
                border:1px solid #294454;
                border-radius:18px 18px 0 0;
                padding:22px 24px 18px;
                text-align:center;
                margin-bottom:-2px;
            ">
                <div style="
                    color:#63bdf4;
                    font-size:.9rem;
                    font-weight:800;
                    letter-spacing:.10em;
                ">
                    {stage["title"]}
                </div>
                <div style="
                    color:white;
                    font-size:2rem;
                    font-weight:900;
                    line-height:1.2;
                    margin-top:.35rem;
                ">
                    {stage["subtitle"].upper()}
                </div>
                <div style="
                    color:#f49ac2;
                    font-size:2.8rem;
                    font-weight:900;
                    line-height:1;
                    margin-top:.65rem;
                ">
                    {display_distance} km
                </div>
                <div style="
                    color:#9fb1bf;
                    font-size:.82rem;
                    letter-spacing:.08em;
                    margin-top:.3rem;
                ">
                    {distance_caption}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = go.Figure()

        if is_stationary:
            fig.add_trace(
                go.Scattermapbox(
                    lat=[start[0]],
                    lon=[start[1]],
                    mode="markers+text",
                    text=[stage["labels"][0][0]],
                    textposition="top right",
                    textfont=dict(size=16, color="#68c2ff"),
                    marker=dict(size=22, color="#36aef5"),
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=[start[0]],
                    lon=[start[1]],
                    mode="text",
                    text=["📍"],
                    textfont=dict(size=32, color="#ffffff"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
        else:
            # Simple route for the active travel day.
            fig.add_trace(
                go.Scattermapbox(
                    lat=[start[0], end[0]],
                    lon=[start[1], end[1]],
                    mode="lines",
                    line=dict(width=7, color="#334e63"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=[start[0], vehicle_lat],
                    lon=[start[1], vehicle_lon],
                    mode="lines",
                    line=dict(width=6, color="#36aef5"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=[vehicle_lat, end[0]],
                    lon=[vehicle_lon, end[1]],
                    mode="lines",
                    line=dict(width=5, color="#ff70b8"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

            # Separate marker traces avoid Plotly textposition errors.
            fig.add_trace(
                go.Scattermapbox(
                    lat=[start[0]],
                    lon=[start[1]],
                    mode="markers+text",
                    text=[stage["labels"][0][0]],
                    textposition="top left",
                    textfont=dict(size=15, color="#68c2ff"),
                    marker=dict(size=18, color="#36aef5"),
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=[end[0]],
                    lon=[end[1]],
                    mode="markers+text",
                    text=[stage["labels"][-1][0]],
                    textposition="bottom right",
                    textfont=dict(size=15, color="#ff8bc5"),
                    marker=dict(size=18, color="#ff70b8"),
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False,
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=[vehicle_lat],
                    lon=[vehicle_lon],
                    mode="text",
                    text=[stage["vehicle"]],
                    textfont=dict(size=36, color="#ffffff"),
                    hovertemplate=f"{stage['vehicle_name']}<extra></extra>",
                    showlegend=False,
                )
            )

        center_lat = (stage["lat_range"][0] + stage["lat_range"][1]) / 2
        center_lon = (stage["lon_range"][0] + stage["lon_range"][1]) / 2
        zoom = 7.1 if is_stationary else (7.0 if state.current_date.day == 12 else 6.3)

        fig.update_layout(
            height=560,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#08131e",
            plot_bgcolor="#08131e",
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom,
            ),
            annotations=[
                dict(
                    x=0.02, y=0.03, xref="paper", yref="paper",
                    text=f"<b>RĂZVAN</b><br><span style='font-size:12px'>{state.location}</span>",
                    showarrow=False, align="left",
                    font=dict(size=18, color="#59b9ff"),
                    bgcolor="rgba(4,15,24,.86)",
                    bordercolor="#2d536b", borderwidth=1, borderpad=8,
                ),
                dict(
                    x=0.98, y=0.03, xref="paper", yref="paper",
                    text="<b>ALEXANDRA</b><br><span style='font-size:12px'>În Ploiești</span>",
                    showarrow=False, align="right", xanchor="right",
                    font=dict(size=18, color="#ff82bf"),
                    bgcolor="rgba(4,15,24,.86)",
                    bordercolor="#67405a", borderwidth=1, borderpad=8,
                ),
            ],
            images=[
                dict(
                    source=_image_data(AVATAR_DIR / "razvan_avatar.png"),
                    xref="paper", yref="paper",
                    x=0.015, y=0.24,
                    sizex=0.11, sizey=0.11,
                    xanchor="left", yanchor="bottom",
                    sizing="contain", opacity=1, layer="above",
                ),
                dict(
                    source=_image_data(AVATAR_DIR / "alexandra_avatar.png"),
                    xref="paper", yref="paper",
                    x=0.985, y=0.24,
                    sizex=0.11, sizey=0.11,
                    xanchor="right", yanchor="bottom",
                    sizing="contain", opacity=1, layer="above",
                ),
            ],
            font=dict(family="Arial, sans-serif"),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": True,
            },
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Faza", state.phase)
        c2.metric("Localizare", state.location)
        c3.metric("Următorul punct", state.next_target)
        c4.metric("Zile rămase", state.days_remaining)
        return

    # Local detailed route: Ploiești -> Brașov.
    # Here both travel together, so the visual language is unified:
    # one route color, one shared origin and one shared "ECHIPAJ" block.
    if stage["title"] == "PROTOCOL PRAHOVA–BRAȘOV":
        start = LOCATIONS["ploiesti"]
        end = LOCATIONS["brasov"]
        vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

        local_distance_km = max(0, round(110 * (1 - stage["progress"])))

        st.markdown(
            f"""
            <div style="
                background:#08131e;
                border:1px solid #294454;
                border-radius:18px 18px 0 0;
                padding:22px 24px 18px;
                text-align:center;
                margin-bottom:-2px;
            ">
                <div style="
                    color:#f2b84b;
                    font-size:.9rem;
                    font-weight:800;
                    letter-spacing:.10em;
                ">
                    PROTOCOL PRAHOVA–BRAȘOV
                </div>
                <div style="
                    color:white;
                    font-size:2rem;
                    font-weight:900;
                    line-height:1.2;
                    margin-top:.35rem;
                ">
                    MISIUNEA: DEPLASARE ÎMPREUNĂ
                </div>
                <div style="
                    color:#f2b84b;
                    font-size:2.8rem;
                    font-weight:900;
                    line-height:1;
                    margin-top:.65rem;
                ">
                    {local_distance_km} km
                </div>
                <div style="
                    color:#9fb1bf;
                    font-size:.82rem;
                    letter-spacing:.08em;
                    margin-top:.3rem;
                ">
                    DISTANȚĂ RUTIERĂ ESTIMATĂ
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = go.Figure()

        # Full route in one unified color.
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0], end[0]],
                lon=[start[1], end[1]],
                mode="lines",
                line=dict(width=7, color="#f2b84b"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # Origin and destination use the same color scheme.
        # Ploiești marker and label.
        fig.add_trace(
            go.Scattermapbox(
                lat=[start[0]],
                lon=[start[1]],
                mode="markers+text",
                text=["Ploiești — plecare împreună"],
                textposition="bottom right",
                textfont=dict(size=15, color="#ffd98d"),
                marker=dict(size=18, color="#f2b84b"),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )

        # Brașov marker and label.
        fig.add_trace(
            go.Scattermapbox(
                lat=[end[0]],
                lon=[end[1]],
                mode="markers+text",
                text=["Brașov — destinație"],
                textposition="top right",
                textfont=dict(size=15, color="#ffd98d"),
                marker=dict(size=18, color="#f2b84b"),
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )

        # Shared vehicle.
        fig.add_trace(
            go.Scattermapbox(
                lat=[vehicle_lat],
                lon=[vehicle_lon],
                mode="text",
                text=["🚆 / 🚗"],
                textfont=dict(size=36, color="#ffffff"),
                hovertemplate="Răzvan + Alexandra — transport de stabilit<extra></extra>",
                showlegend=False,
            )
        )

        fig.update_layout(
            height=540,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#08131e",
            plot_bgcolor="#08131e",
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=45.28, lon=25.80),
                zoom=7.15,
            ),
            annotations=[
                dict(
                    x=0.02, y=0.03, xref="paper", yref="paper",
                    text="<b>ECHIPAJ</b><br><span style='font-size:12px'>Răzvan + Alexandra</span><br><span style='font-size:11px'>Plecare împreună din Ploiești</span>",
                    showarrow=False, align="left",
                    font=dict(size=18, color="#ffd98d"),
                    bgcolor="rgba(4,15,24,.86)",
                    bordercolor="#7a6330", borderwidth=1, borderpad=8,
                ),
            ],
            images=[
                dict(
                    source=_image_data(AVATAR_DIR / "razvan_avatar.png"),
                    xref="paper", yref="paper",
                    x=0.015, y=0.24,
                    sizex=0.11, sizey=0.11,
                    xanchor="left", yanchor="bottom",
                    sizing="contain", opacity=1, layer="above",
                ),
                dict(
                    source=_image_data(AVATAR_DIR / "alexandra_avatar.png"),
                    xref="paper", yref="paper",
                    x=0.085, y=0.24,
                    sizex=0.11, sizey=0.11,
                    xanchor="left", yanchor="bottom",
                    sizing="contain", opacity=1, layer="above",
                ),
            ],
            font=dict(family="Arial, sans-serif"),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": True,
            },
        )

        st.markdown(
            """
            <style>
            .sata-local-cards {
                display:grid;
                grid-template-columns:repeat(4,minmax(0,1fr));
                gap:12px;
                margin-top:8px;
                margin-bottom:8px;
            }
            .sata-local-card {
                background:#0b1722;
                border:1px solid #294454;
                border-radius:14px;
                padding:14px 16px;
                min-height:88px;
            }
            .sata-local-label {
                color:#8195a4;
                font-size:.78rem;
                margin-bottom:7px;
            }
            .sata-local-value {
                color:#f4f7fa;
                font-size:1.35rem;
                line-height:1.2;
                font-weight:800;
                white-space:normal;
                overflow-wrap:anywhere;
            }
            @media(max-width:760px) {
                .sata-local-cards {grid-template-columns:1fr 1fr;}
            }
            </style>
            <div class="sata-local-cards">
              <div class="sata-local-card">
                <div class="sata-local-label">Faza</div>
                <div class="sata-local-value">Ploiești → Brașov</div>
              </div>
              <div class="sata-local-card">
                <div class="sata-local-label">Echipaj</div>
                <div class="sata-local-value">Răzvan + Alexandra</div>
              </div>
              <div class="sata-local-card">
                <div class="sata-local-label">Transport</div>
                <div class="sata-local-value">De stabilit</div>
              </div>
              <div class="sata-local-card">
                <div class="sata-local-label">Destinație</div>
                <div class="sata-local-value">Brașov</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Europe overview: the detailed map is the background of the entire panel.
    start = stage["start"]
    end = stage["end"]

    # Before 9 August the flight has not started, so the aircraft stays at origin.
    vehicle_lat, vehicle_lon = start
    razvan_uri = _image_data(AVATAR_DIR / "razvan_avatar.png")
    alexandra_uri = _image_data(AVATAR_DIR / "alexandra_avatar.png")

    fig = go.Figure()

    # Soft route shadow, followed by the operational dotted route.
    fig.add_trace(
        go.Scattermapbox(
            lat=[start[0], end[0]],
            lon=[start[1], end[1]],
            mode="lines",
            line=dict(width=8, color="rgba(7,19,30,.60)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    # Scattermapbox does not support line.dash. Build the dotted route
    # from short visible segments separated by gaps.
    route_lat: list[float | None] = []
    route_lon: list[float | None] = []
    segment_count = 34

    for index in range(segment_count):
        start_t = index / segment_count
        end_t = min(1.0, start_t + 0.52 / segment_count)

        lat_a = start[0] + (end[0] - start[0]) * start_t
        lon_a = start[1] + (end[1] - start[1]) * start_t
        lat_b = start[0] + (end[0] - start[0]) * end_t
        lon_b = start[1] + (end[1] - start[1]) * end_t

        route_lat.extend([lat_a, lat_b, None])
        route_lon.extend([lon_a, lon_b, None])

    fig.add_trace(
        go.Scattermapbox(
            lat=route_lat,
            lon=route_lon,
            mode="lines",
            line=dict(width=4, color="#ff70b8"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            lat=[start[0]],
            lon=[start[1]],
            mode="markers+text",
            text=["Amersfoort"],
            textposition="top left",
            textfont=dict(size=15, color="#69c5ff"),
            marker=dict(size=17, color="#36aef5"),
            hovertemplate="Amersfoort<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            lat=[end[0]],
            lon=[end[1]],
            mode="markers+text",
            text=["Ploiești"],
            textposition="bottom right",
            textfont=dict(size=15, color="#ff8bc5"),
            marker=dict(size=17, color="#ff70b8"),
            hovertemplate="Ploiești<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            lat=[vehicle_lat],
            lon=[vehicle_lon],
            mode="text",
            text=["✈"],
            textfont=dict(size=35, color="#ffffff"),
            hovertemplate="Zborul nu a început<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#08131e",
        plot_bgcolor="#08131e",
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=48.6, lon=14.5),
            zoom=3.35,
        ),
        shapes=[
            # One stable background plate; each text line is positioned separately.
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0.24,
                x1=0.76,
                y0=0.835,
                y1=0.99,
                fillcolor="rgba(4,15,24,.82)",
                line=dict(color="rgba(52,116,157,.50)", width=1),
                layer="above",
            ),
        ],
        annotations=[
            dict(
                x=0.5, y=0.968, xref="paper", yref="paper",
                text=f"<b>{stage['title']}</b>",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                align="center",
                font=dict(size=13, color="#63bdf4"),
            ),
            dict(
                x=0.5, y=0.925, xref="paper", yref="paper",
                text="<b>MISIUNEA: APROPIERE EMOȚIONALĂ</b>",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                align="center",
                font=dict(size=27, color="#ffffff"),
            ),
            dict(
                x=0.5, y=0.875, xref="paper", yref="paper",
                text=f"<b>{state.distance_km} km</b>",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                align="center",
                font=dict(size=43, color="#f49ac2"),
            ),
            dict(
                x=0.5, y=0.842, xref="paper", yref="paper",
                text="DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                align="center",
                font=dict(size=12, color="#b6c5cf"),
            ),
            dict(
                x=0.02, y=0.035, xref="paper", yref="paper",
                text="<b>RĂZVAN</b><br><span style='font-size:12px'>Amersfoort, Olanda</span>",
                showarrow=False, align="left",
                font=dict(size=18, color="#59b9ff"),
                bgcolor="rgba(4,15,24,.86)",
                bordercolor="#2d536b", borderwidth=1, borderpad=8,
            ),
            dict(
                x=0.98, y=0.035, xref="paper", yref="paper",
                text="<b>ALEXANDRA</b><br><span style='font-size:12px'>Ploiești, România</span>",
                showarrow=False, align="right", xanchor="right",
                font=dict(size=18, color="#ff82bf"),
                bgcolor="rgba(4,15,24,.86)",
                bordercolor="#67405a", borderwidth=1, borderpad=8,
            ),
        ],
        images=[
            dict(
                source=razvan_uri,
                xref="paper", yref="paper",
                x=0.015, y=0.245,
                sizex=0.13, sizey=0.13,
                xanchor="left", yanchor="bottom",
                sizing="contain", opacity=1, layer="above",
            ),
            dict(
                source=alexandra_uri,
                xref="paper", yref="paper",
                x=0.985, y=0.245,
                sizex=0.13, sizey=0.13,
                xanchor="right", yanchor="bottom",
                sizing="contain", opacity=1, layer="above",
            ),
        ],
        font=dict(family="Arial, sans-serif"),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "scrollZoom": True,
        },
    )

    # Custom responsive cards prevent long values from being truncated.
    st.markdown(
        f"""
        <style>
        .eu-status-grid {{
            display:grid;
            grid-template-columns:repeat(4,minmax(0,1fr));
            gap:12px;
            margin-top:8px;
        }}
        .eu-status-card {{
            background:#0b1722;
            border:1px solid #294454;
            border-radius:14px;
            padding:14px 16px;
            min-width:0;
        }}
        .eu-status-label {{
            color:#8195a4;
            font-size:.77rem;
            margin-bottom:7px;
        }}
        .eu-status-value {{
            color:#f4f7fa;
            font-size:clamp(1rem,2vw,1.35rem);
            line-height:1.22;
            font-weight:850;
            overflow-wrap:anywhere;
            white-space:normal;
        }}
        @media(max-width:760px) {{
            .eu-status-grid {{grid-template-columns:1fr 1fr;}}
        }}
        </style>

        <div class="eu-status-grid">
          <div class="eu-status-card">
            <div class="eu-status-label">Faza</div>
            <div class="eu-status-value">{state.phase}</div>
          </div>
          <div class="eu-status-card">
            <div class="eu-status-label">Vehicul</div>
            <div class="eu-status-value">{stage["vehicle_name"]}</div>
          </div>
          <div class="eu-status-card">
            <div class="eu-status-label">Următorul punct</div>
            <div class="eu-status-value">{state.next_target}</div>
          </div>
          <div class="eu-status-card">
            <div class="eu-status-label">Progres total</div>
            <div class="eu-status-value">{state.progress_percent}%</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
