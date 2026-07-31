from __future__ import annotations

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

    if current.month == 8 and current.day < 14:
        start = LOCATIONS["cluj"]
        end = LOCATIONS["ploiesti"]
        progress = max(0.0, min(1.0, (state.progress_percent - 45) / 40))
        return {
            "title": "PROTOCOL ROMÂNIA",
            "subtitle": "Cluj-Napoca → Ploiești",
            "start": start,
            "end": end,
            "vehicle": "🚗",
            "vehicle_name": "Mașină",
            "progress": progress,
            "lat_range": [43.4, 48.5],
            "lon_range": [19.5, 29.8],
            "labels": [("Cluj-Napoca", start), ("Ploiești", end)],
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


def render_mission_map(state: MissionState) -> None:
    stage = _stage(state)
    start = stage["start"]
    end = stage["end"]
    vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

    fig = go.Figure()

    # Route shadow
    fig.add_trace(
        go.Scattergeo(
            lat=[start[0], end[0]],
            lon=[start[1], end[1]],
            mode="lines",
            line=dict(width=8, color="rgba(22, 45, 65, 0.85)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Active route
    fig.add_trace(
        go.Scattergeo(
            lat=[start[0], vehicle_lat],
            lon=[start[1], vehicle_lon],
            mode="lines",
            line=dict(width=5, color="#36aef5"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Remaining route
    fig.add_trace(
        go.Scattergeo(
            lat=[vehicle_lat, end[0]],
            lon=[vehicle_lon, end[1]],
            mode="lines",
            line=dict(width=4, color="#ff70b8", dash="dot"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # City markers
    city_lats = [item[1][0] for item in stage["labels"]]
    city_lons = [item[1][1] for item in stage["labels"]]
    city_names = [item[0] for item in stage["labels"]]

    fig.add_trace(
        go.Scattergeo(
            lat=city_lats,
            lon=city_lons,
            mode="markers+text",
            text=city_names,
            textposition=["top left", "top right"],
            textfont=dict(size=15, color=["#68c2ff", "#ff8bc5"]),
            marker=dict(
                size=15,
                color=["#35aef5", "#ff70b8"],
                line=dict(width=3, color="#eef8ff"),
            ),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # Vehicle
    fig.add_trace(
        go.Scattergeo(
            lat=[vehicle_lat],
            lon=[vehicle_lon],
            mode="text",
            text=[stage["vehicle"]],
            textfont=dict(size=34, color="#ffffff"),
            hovertemplate=f"{stage['vehicle_name']}<extra></extra>",
            showlegend=False,
        )
    )

    # Alexandra remains visible on the Romania map, even while the vehicle starts in Cluj.
    if stage["title"] == "PROTOCOL ROMÂNIA":
        ploiesti = LOCATIONS["ploiesti"]
        fig.add_trace(
            go.Scattergeo(
                lat=[ploiesti[0]],
                lon=[ploiesti[1]],
                mode="markers",
                marker=dict(size=22, color="rgba(255,112,184,.20)", line=dict(width=2, color="#ff70b8")),
                hoverinfo="skip",
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
        countrywidth=1.1,
        showcoastlines=True,
        coastlinecolor="#34749d",
        coastlinewidth=1.2,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
        lataxis_range=stage["lat_range"],
        lonaxis_range=stage["lon_range"],
        resolution=50,
    )

    fig.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=105, b=20),
        paper_bgcolor="#08131e",
        plot_bgcolor="#08131e",
        title=dict(
            text=(
                f"<span style='font-size:14px;color:#63bdf4'>{stage['title']}</span><br>"
                f"<span style='font-size:28px;color:white'><b>MISIUNEA: APROPIERE EMOȚIONALĂ</b></span><br>"
                f"<span style='font-size:46px;color:#f49ac2'><b>{state.distance_km} km</b></span><br>"
                f"<span style='font-size:13px;color:#9fb1bf'>DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ</span>"
            ),
            x=0.5,
            xanchor="center",
            y=0.98,
            yanchor="top",
        ),
        annotations=[
            dict(
                x=0.02, y=0.02, xref="paper", yref="paper",
                text="<b>RĂZVAN</b><br><span style='font-size:12px'>Amersfoort, Olanda</span>",
                showarrow=False, align="left",
                font=dict(size=18, color="#59b9ff"),
                bgcolor="rgba(4,15,24,.78)", bordercolor="#2d536b", borderwidth=1, borderpad=8,
            ),
            dict(
                x=0.98, y=0.02, xref="paper", yref="paper",
                text="<b>ALEXANDRA</b><br><span style='font-size:12px'>Ploiești, România</span>",
                showarrow=False, align="right",
                xanchor="right",
                font=dict(size=18, color="#ff82bf"),
                bgcolor="rgba(4,15,24,.78)", bordercolor="#67405a", borderwidth=1, borderpad=8,
            ),
        ],
        images=[
            dict(
                source=_image_data(AVATAR_DIR / "razvan_avatar.png"),
                xref="paper", yref="paper",
                x=0.015, y=0.28,
                sizex=0.17, sizey=0.17,
                xanchor="left", yanchor="bottom",
                sizing="contain", opacity=1, layer="above",
            ),
            dict(
                source=_image_data(AVATAR_DIR / "alexandra_avatar.png"),
                xref="paper", yref="paper",
                x=0.985, y=0.28,
                sizex=0.17, sizey=0.17,
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
            "scrollZoom": False,
        },
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faza", state.phase)
    c2.metric("Vehicul", stage["vehicle_name"])
    c3.metric("Următorul punct", state.next_target)
    c4.metric("Progres total", f"{state.progress_percent}%")
