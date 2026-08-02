from __future__ import annotations

from datetime import date
import hashlib
import random
import time

import streamlit as st

from core.mission_state import MissionState


SCAN_STEPS = [
    "Inițializare sateliți...",
    "Căutare semnal emoțional...",
    "Localizare Alexandra...",
    "Analiză nivel de calm declarat...",
    "Comparare cu nivelul de calm probabil...",
    "Detectare urme de sarcasm...",
    "Estimare număr de scenarii imaginare...",
    "Verificare protocol «Vedem...»...",
    "Corelare cu distanța față de Răzvan...",
    "Generare concluzie clasificată...",
]


EUROPE_RESULTS = [
    ("CALM SUSPECT", "Alexandra pare liniștită. Sistemul consideră această informație insuficient de credibilă.", 38),
    ("NERĂBDARE ASCUNSĂ", "S-au detectat semne discrete de curiozitate. Subiectul continuă să pretindă că totul este normal.", 52),
    ("NEGARE FUNCȚIONALĂ", "Nivelul de panică este redus. Nivelul de gânduri despre august este semnificativ mai mare.", 47),
    ("MONITORIZARE ACTIVĂ", "Alexandra pare relaxată, dar verifică mental calendarul mai des decât ar recunoaște.", 44),
]

ROMANIA_RESULTS = [
    ("PRECIZIE CRESCUTĂ", "Răzvan se află în aceeași țară. Scannerul raportează o creștere bruscă a relevanței datelor.", 66),
    ("EMOȚII ÎN CREȘTERE", "Distanța s-a redus. Numărul scenariilor posibile nu a urmat aceeași tendință.", 71),
    ("CALM DECLARAT", "Alexandra afirmă că situația este sub control. Sistemul a notat declarația fără să o creadă complet.", 63),
    ("APROPIERE DETECTATĂ", "Semnalul emoțional este mai puternic. Cauza probabilă: România a devenit brusc prea mică.", 74),
]

PLOIESTI_RESULTS = [
    ("CONTACT APROPIAT", "Distanța operațională este zero. Algoritmii S.A.T.A. au devenit vizibil mai puțin siguri pe ei.", 87),
    ("ZÂMBETE DETECTATE", "Scannerul raportează o probabilitate ridicată de tachinare și o probabilitate foarte mică de plictiseală.", 82),
    ("ANALIZĂ INSTABILĂ", "Alexandra se află prea aproape pentru o analiză obiectivă. Se recomandă observație directă.", 91),
    ("PROTOCOL PLOIEȘTI", "Nivelul emoțional este ridicat, dar sistemul nu detectează niciun motiv real de alarmă.", 79),
]

BRASOV_RESULTS = [
    ("MODELE DEPĂȘITE", "Sistemul nu poate prezice ce urmează. Realitatea a refuzat să respecte toate simulările.", 96),
    ("PROTOCOL CARPAȚI", "S-au detectat emoții, glume și posibilitatea unor amintiri bune. Scanarea continuă.", 93),
    ("ANALIZĂ IMPOSIBILĂ", "Alexandra pare să se distreze. S.A.T.A. consideră aceasta o anomalie pozitivă.", 89),
    ("STARE NECALCULABILĂ", "Toate modelele au cedat. Se recomandă continuarea weekendului fără intervenție tehnică.", 98),
]

RARE_RESULTS = [
    ("EROARE 418", "Alexandra a observat că este scanată. Retragere tactică recomandată.", None),
    ("ACCES REFUZAT", "Starea Alexandrei este clasificată. Nivelul actual de autorizare este insuficient.", None),
    ("ANOMALIE", "Scannerul a detectat o glumă înainte ca aceasta să fie spusă. Rezultatul este sub investigație.", None),
    ("SCANARE ÎNTRERUPTĂ", "Subiectul analizat pare imposibil de încadrat într-un singur procent. Reîncercați după cafea.", None),
]


def _seed(state: MissionState, scan_count: int) -> int:
    raw = f"{state.current_date.isoformat()}::{scan_count}".encode("utf-8")
    return int(hashlib.sha256(raw).hexdigest()[:12], 16)


def _result_pool(state: MissionState):
    if date(2026, 8, 15) <= state.current_date <= date(2026, 8, 17):
        return BRASOV_RESULTS
    if state.current_date >= date(2026, 8, 14):
        return PLOIESTI_RESULTS
    if state.current_date >= date(2026, 8, 9):
        return ROMANIA_RESULTS
    return EUROPE_RESULTS


def _render_result(title: str, text: str, score: int | None) -> None:
    score_html = (
        f"""
        <div class="scan-score">{score}%</div>
        <div class="scan-score-label">NIVEL EMOȚIONAL ESTIMAT</div>
        """
        if score is not None
        else """
        <div class="scan-score">???</div>
        <div class="scan-score-label">VALOARE INDISPONIBILĂ</div>
        """
    )

    st.markdown(
        f"""
        <div class="scan-result">
          <div class="scan-result-label">REZULTAT SCANARE</div>
          <div class="scan-result-title">{title}</div>
          {score_html}
          <div class="scan-result-text">{text}</div>
          <div class="scan-disclaimer">
            Concluzie generată de S.A.T.A. cu o precizie imposibil de verificat.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_emotion_scanner(state: MissionState) -> None:
    st.markdown(
        """
        <style>
        .scanner-shell {
            margin-top:16px;
            padding:20px;
            border-radius:17px;
            color:white;
            background:
                radial-gradient(circle at 80% 15%, rgba(255,112,184,.13), transparent 35%),
                radial-gradient(circle at 20% 80%, rgba(54,174,245,.14), transparent 35%),
                linear-gradient(145deg,#07131d,#111d28);
            border:1px solid #2f4b5d;
        }
        .scanner-kicker {
            color:#63bdf4;
            font-size:.78rem;
            font-weight:900;
            letter-spacing:.12em;
        }
        .scanner-title {
            margin-top:.35rem;
            font-size:clamp(1.45rem,5vw,2rem);
            font-weight:950;
        }
        .scanner-text {
            margin-top:.55rem;
            color:#a8bac7;
            line-height:1.45;
        }
        .scanner-lights {
            display:flex;
            gap:7px;
            margin-top:14px;
        }
        .scanner-lights span {
            width:11px;
            height:11px;
            border-radius:50%;
            background:#253b49;
            box-shadow:0 0 0 rgba(54,174,245,0);
        }
        .scanner-lights span:nth-child(1),
        .scanner-lights span:nth-child(3),
        .scanner-lights span:nth-child(6) {
            background:#36aef5;
            box-shadow:0 0 12px rgba(54,174,245,.65);
        }
        .scanner-lights span:nth-child(2),
        .scanner-lights span:nth-child(5) {
            background:#ff70b8;
            box-shadow:0 0 12px rgba(255,112,184,.55);
        }
        .scan-result {
            margin-top:14px;
            padding:22px;
            border-radius:16px;
            text-align:center;
            color:white;
            background:linear-gradient(145deg,#0b1722,#152636);
            border:1px solid #35566b;
        }
        .scan-result-label {
            color:#63bdf4;
            font-size:.75rem;
            font-weight:900;
            letter-spacing:.12em;
        }
        .scan-result-title {
            margin-top:.45rem;
            font-size:clamp(1.4rem,5vw,2rem);
            font-weight:950;
            color:#ffd98d;
        }
        .scan-score {
            margin-top:.75rem;
            font-size:clamp(3rem,12vw,4.8rem);
            line-height:1;
            font-weight:950;
            color:#ff82bf;
        }
        .scan-score-label {
            color:#96aab8;
            font-size:.72rem;
            letter-spacing:.08em;
            margin-top:.25rem;
        }
        .scan-result-text {
            margin:1rem auto 0;
            max-width:760px;
            font-size:1.08rem;
            line-height:1.55;
            font-weight:750;
        }
        .scan-disclaimer {
            margin-top:1rem;
            color:#7f95a4;
            font-size:.75rem;
        }
        </style>

        <div class="scanner-shell">
          <div class="scanner-kicker">INSTRUMENT EXPERIMENTAL • EMOTION SCANNER</div>
          <div class="scanner-title">🛰 Scanează starea actuală a Alexandrei</div>
          <div class="scanner-text">
            Apasă butonul pentru a iniția o analiză complet neautorizată și aproximativ științifică.
          </div>
          <div class="scanner-lights">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "▶ INIȚIAZĂ SCANAREA",
        use_container_width=True,
        type="primary",
        key="emotion_scan_button",
    ):
        scan_count = st.session_state.get("emotion_scan_count", 0) + 1
        st.session_state["emotion_scan_count"] = scan_count

        status = st.empty()
        progress = st.progress(0)

        rng = random.Random(_seed(state, scan_count))
        steps = SCAN_STEPS.copy()
        rng.shuffle(steps)

        for index, step in enumerate(steps[:8], start=1):
            status.info(step)
            progress.progress(index / 8)
            time.sleep(0.28)

        status.success("Scanare finalizată.")
        time.sleep(0.35)

        if rng.random() < 0.12:
            title, text, score = rng.choice(RARE_RESULTS)
        else:
            title, text, score = rng.choice(_result_pool(state))

        st.session_state["emotion_scan_result"] = (title, text, score)

    result = st.session_state.get("emotion_scan_result")
    if result:
        _render_result(*result)
