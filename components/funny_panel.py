from __future__ import annotations

from datetime import date
import hashlib
import random

import streamlit as st

from core.mission_state import MissionState


GENERAL_MESSAGES = [
    "Alexandra afirmă că este perfect calmă. S.A.T.A. a înregistrat declarația și a pornit simultan trei verificări.",
    "Telefonul a fost verificat din nou. Nu s-au detectat mesaje noi, dar procedura va fi repetată în curând.",
    "Nivelul de «vedem noi» rămâne ridicat și stabil.",
    "Sistemul detectează o cantitate neobișnuită de gânduri de tipul «dar dacă...».",
    "Cafeaua nu reduce emoțiile. Doar le oferă o viteză de procesare mai mare.",
    "Prognoza meteo a fost verificată suficient. Vremea refuză în continuare să garanteze ceva.",
    "S.A.T.A. recomandă evitarea analizării fiecărei pauze de răspuns ca pe un incident diplomatic.",
    "Nivelul de negare este în limite normale pentru o persoană care susține că nu este emoționată.",
]

PHRASE_PROBABILITIES = [
    ("„Vedem.”", 91, "Traducere estimată: există deja cel puțin trei scenarii."),
    ("„Nu sunt stresată.”", 97, "Credibilitate estimată de sistem: 3%."),
    ("„Lasă...”", 84, "S.A.T.A. recomandă să nu insiste nimeni."),
    ("„Nu contează.”", 93, "Evaluare internă: probabil contează."),
    ("„Mai vorbim.”", 82, "Subiectul rămâne deschis și monitorizat."),
]

RECOMMENDATIONS = [
    "Respirația rămâne o funcție recomandată de sistem.",
    "Telefonul nu răspunde mai repede dacă este privit continuu.",
    "Nu toate momentele importante trebuie planificate.",
    "Păstrați nivelul de panică sub 80%. Restul este negociabil.",
    "Sistemul recomandă mai puține scenarii și mai multă realitate.",
    "Nu există niciun cronometru.",
    "Weekendul nu are obiective obligatorii. Doar posibilități.",
    "Dacă planul se schimbă, aplicația va pretinde că a prevăzut asta.",
]

SPECIAL_MESSAGES = {
    date(2026, 8, 9): (
        "EVENIMENT MAJOR",
        "Răzvan a intrat pe teritoriul României. Alexandra declară că situația este sub control. Sistemul rămâne sceptic.",
    ),
    date(2026, 8, 12): (
        "DEPLASARE INTERNĂ",
        "Subiectul părăsește Cluj-Napoca. Nivelul de proximitate crește. Nivelul de calm declarat rămâne suspect de constant.",
    ),
    date(2026, 8, 13): (
        "STAȚIONARE TÂRGU MUREȘ",
        "Ultima oprire înainte de Ploiești. S.A.T.A. recomandă reducerea simulărilor mentale la maximum 12 pe oră.",
    ),
    date(2026, 8, 14): (
        "CONTACT ÎN PLOIEȘTI",
        "Distanța operațională a fost redusă la zero. Sistemul nu garantează că și emoțiile vor urma aceeași tendință.",
    ),
    date(2026, 8, 15): (
        "OPERAȚIUNEA BRAȘOV",
        "Sistemul suspendă predicțiile. Motiv oficial: realitatea urmează să fie observată direct.",
    ),
}


def _seed(state: MissionState, salt: str) -> int:
    key = f"{state.current_date.isoformat()}::{salt}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:12], 16)


def _panic_value(state: MissionState) -> int:
    if state.current_date < date(2026, 8, 9):
        days = max(0, (date(2026, 8, 9) - state.current_date).days)
        return max(22, 58 - days * 4)
    if state.current_date <= date(2026, 8, 11):
        return 61
    if state.current_date == date(2026, 8, 12):
        return 68
    if state.current_date == date(2026, 8, 13):
        return 76
    if state.current_date == date(2026, 8, 14):
        return 88
    if date(2026, 8, 15) <= state.current_date <= date(2026, 8, 17):
        return 96
    return 54


def render_funny_panel(state: MissionState) -> None:
    rng_message = random.Random(_seed(state, "message"))
    rng_phrase = random.Random(_seed(state, "phrase"))
    rng_recommendation = random.Random(_seed(state, "recommendation"))

    special = SPECIAL_MESSAGES.get(state.current_date)
    if special:
        bulletin_title, bulletin_text = special
    else:
        bulletin_title = "BULETIN OPERATIV"
        bulletin_text = rng_message.choice(GENERAL_MESSAGES)

    phrase, probability, phrase_note = rng_phrase.choice(PHRASE_PROBABILITIES)
    recommendation = rng_recommendation.choice(RECOMMENDATIONS)
    panic = _panic_value(state)
    denial = min(99, panic + 6)
    phone_checks = max(4, round(panic / 4))

    st.markdown(
        f"""
        <style>
        .funny-grid {{
            display:grid;
            grid-template-columns:1.35fr 1fr;
            gap:14px;
            margin-top:18px;
        }}
        .funny-card {{
            background:#0b1722;
            border:1px solid #294454;
            border-radius:16px;
            padding:20px;
            color:#f4f7fa;
            min-height:170px;
        }}
        .funny-title {{
            color:#55b9ff;
            font-size:.8rem;
            font-weight:900;
            letter-spacing:.12em;
            margin-bottom:10px;
        }}
        .funny-main {{
            font-size:1.25rem;
            line-height:1.45;
            font-weight:750;
        }}
        .funny-muted {{
            color:#93a8b7;
            margin-top:9px;
            line-height:1.4;
        }}
        .funny-number {{
            font-size:3rem;
            line-height:1;
            font-weight:950;
            color:#ff82bf;
            margin:.3rem 0 .6rem;
        }}
        .indicator-grid {{
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:12px;
            margin-top:14px;
        }}
        .indicator-card {{
            background:#09131d;
            border:1px solid #243c4b;
            border-radius:14px;
            padding:15px;
        }}
        .indicator-label {{
            color:#8195a4;
            font-size:.75rem;
            margin-bottom:6px;
        }}
        .indicator-value {{
            color:#f2b84b;
            font-size:1.55rem;
            font-weight:900;
        }}
        .recommendation-card {{
            background:#fff3cf;
            color:#25313a;
            border-radius:16px;
            padding:20px;
            margin-top:14px;
            border:1px solid #d8bd67;
        }}
        .recommendation-card .funny-title {{
            color:#775c14;
        }}
        @media(max-width:800px) {{
            .funny-grid {{grid-template-columns:1fr;}}
            .indicator-grid {{grid-template-columns:1fr;}}
        }}
        </style>

        <div class="funny-grid">
          <div class="funny-card">
            <div class="funny-title">{bulletin_title}</div>
            <div class="funny-main">{bulletin_text}</div>
            <div class="indicator-grid">
              <div class="indicator-card">
                <div class="indicator-label">Probabilitate panică</div>
                <div class="indicator-value">{panic}%</div>
              </div>
              <div class="indicator-card">
                <div class="indicator-label">Nivel negare</div>
                <div class="indicator-value">{denial}%</div>
              </div>
              <div class="indicator-card">
                <div class="indicator-label">Verificări telefon estimate</div>
                <div class="indicator-value">{phone_checks}/oră</div>
              </div>
            </div>
          </div>

          <div class="funny-card">
            <div class="funny-title">PROBABILITATEA CA ALEXANDRA SĂ SPUNĂ</div>
            <div class="funny-main">{phrase}</div>
            <div class="funny-number">{probability}%</div>
            <div class="funny-muted">{phrase_note}</div>
          </div>
        </div>

        <div class="recommendation-card">
          <div class="funny-title">RECOMANDAREA S.A.T.A.</div>
          <div class="funny-main">{recommendation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
