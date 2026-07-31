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

    # Local detailed route: Ploiești -> Brașov.
    # Here both travel together, so the visual language is unified:
    # one route color, one shared origin and one shared "ECHIPAJ" block.
    if stage["title"] == "PROTOCOL PRAHOVA–BRAȘOV":
        start = LOCATIONS["ploiesti"]
        end = LOCATIONS["brasov"]
        vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

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
            height=650,
            margin=dict(l=0, r=0, t=155, b=20),
            paper_bgcolor="#08131e",
            plot_bgcolor="#08131e",
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=45.28, lon=25.80),
                zoom=7.7,
            ),
            annotations=[
                dict(
                    x=0.5, y=1.10, xref="paper", yref="paper",
                    text="<span style='font-size:14px;color:#f2b84b'><b>PROTOCOL PRAHOVA–BRAȘOV</b></span>",
                    showarrow=False, xanchor="center", yanchor="top",
                ),
                dict(
                    x=0.5, y=1.04, xref="paper", yref="paper",
                    text="<span style='font-size:27px;color:white'><b>MISIUNEA: DEPLASARE ÎMPREUNĂ</b></span>",
                    showarrow=False, xanchor="center", yanchor="top",
                ),
                dict(
                    x=0.5, y=0.96, xref="paper", yref="paper",
                    text=f"<span style='font-size:42px;color:#f2b84b'><b>{state.distance_km} km</b></span>",
                    showarrow=False, xanchor="center", yanchor="top",
                ),
                dict(
                    x=0.5, y=0.90, xref="paper", yref="paper",
                    text="<span style='font-size:13px;color:#9fb1bf'>DISTANȚĂ RUTIERĂ ESTIMATĂ</span>",
                    showarrow=False, xanchor="center", yanchor="top",
                ),
                dict(
                    x=0.02, y=0.02, xref="paper", yref="paper",
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

    # Europe and Romania overview maps.
    start = stage["start"]
    end = stage["end"]
    vehicle_lat, vehicle_lon = _interpolate(start, end, stage["progress"])

    fig = go.Figure()

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

    fig.update_geos(
        domain=dict(x=[0.0, 1.0], y=[0.0, 0.76]),
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
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor="#08131e",
        plot_bgcolor="#08131e",
        title=dict(text=""),
        annotations=[
            dict(
                x=0.5, y=0.985, xref="paper", yref="paper",
                text=f"<span style='font-size:14px;color:#63bdf4'><b>{stage['title']}</b></span>",
                showarrow=False, xanchor="center", yanchor="top",
            ),
            dict(
                x=0.5, y=0.935, xref="paper", yref="paper",
                text="<span style='font-size:27px;color:white'><b>MISIUNEA: APROPIERE EMOȚIONALĂ</b></span>",
                showarrow=False, xanchor="center", yanchor="top",
            ),
            dict(
                x=0.5, y=0.855, xref="paper", yref="paper",
                text=f"<span style='font-size:42px;color:#f49ac2'><b>{state.distance_km} km</b></span>",
                showarrow=False, xanchor="center", yanchor="top",
            ),
            dict(
                x=0.5, y=0.790, xref="paper", yref="paper",
                text="<span style='font-size:13px;color:#9fb1bf'>DISTANȚĂ OPERAȚIONALĂ ESTIMATĂ</span>",
                showarrow=False, xanchor="center", yanchor="top",
            ),
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
                x=0.015, y=0.24,
                sizex=0.17, sizey=0.17,
                xanchor="left", yanchor="bottom",
                sizing="contain", opacity=1, layer="above",
            ),
            dict(
                source=_image_data(AVATAR_DIR / "alexandra_avatar.png"),
                xref="paper", yref="paper",
                x=0.985, y=0.24,
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
