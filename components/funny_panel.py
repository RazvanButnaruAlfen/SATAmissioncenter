from __future__ import annotations

from datetime import date
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
    "Nu s-au detectat deplasări majore. Gândurile au parcurs însă o distanță considerabilă.",
    "Toate sistemele sunt stabile. Curiozitatea continuă să ruleze fără autorizație.",
    "S.A.T.A. a analizat situația. Situația a refuzat să fie analizată.",
    "S-au detectat zâmbete posibile. Confirmarea vizuală rămâne clasificată.",
]

PHRASE_PROBABILITIES = [
    ("„Vedem.”", (84, 96), "Traducere estimată: există deja cel puțin trei scenarii."),
    ("„Nu sunt stresată.”", (90, 99), "Evaluarea credibilității: foarte creativă."),
    ("„Lasă...”", (76, 91), "S.A.T.A. recomandă să nu insiste nimeni."),
    ("„Nu contează.”", (86, 97), "Evaluare internă: probabil contează."),
    ("„Mai vorbim.”", (74, 90), "Subiectul rămâne deschis și monitorizat."),
    ("„Sunt foarte calmă.”", (88, 99), "Sistemul a pornit automat o verificare suplimentară."),
    ("„Nu mă gândesc la asta.”", (91, 99), "Afirmația a fost mutată în dosarul «optimism suspect»."),
]

RECOMMENDATIONS = [
    "Respirația rămâne o funcție recomandată de S.A.T.A.",
    "Telefonul nu răspunde mai repede dacă este privit continuu.",
    "Nu toate momentele importante trebuie planificate.",
    "Păstrați nivelul de panică sub 80%. Restul este negociabil.",
    "Sistemul recomandă mai puține scenarii imaginare și mai mult contact cu realitatea.",
    "Nu există niciun cronometru. S.A.T.A. a verificat de două ori.",
    "Weekendul nu are obiective obligatorii. Doar posibilități.",
    "Dacă planul se schimbă, aplicația va pretinde că a prevăzut asta.",
    "Luați lucrurile pe rând. Algoritmii care au încercat altfel sunt acum în mentenanță.",
    "O cafea poate ajuta. Trei cafele pot produce o nouă problemă.",
    "Sistemul recomandă o glumă bună și o reducere temporară a analizelor.",
    "Nu transformați fiecare tăcere într-un document clasificat.",
    "Uneori cea mai bună strategie este să vedeți ce se întâmplă.",
    "S.A.T.A. recomandă păstrarea unei aparențe rezonabile de calm.",
    "Nicio decizie importantă nu trebuie luată înainte de micul dejun.",
]

SUMMARIES = [
    "Situația rămâne stabilă, interesantă și imposibil de măsurat corect.",
    "Conexiunea este confirmată. Restul datelor sunt în curs de inventare.",
    "Nu există motive reale de alarmă. Există însă suficiente motive de curiozitate.",
    "S.A.T.A. estimează că lucrurile merg bine. Acuratețea acestei afirmații este clasificată.",
    "Misiunea continuă conform planului, inclusiv acolo unde nu există un plan.",
    "Nivelul general este pozitiv. Nivelul de supra-analiză rămâne impresionant.",
    "Toate drumurile duc spre România. Unele gânduri au ajuns deja.",
    "Concluzie provizorie: mai puțină panică, mai multe momente bune.",
    "Sistemul nu poate prezice finalul. Consideră acest lucru o îmbunătățire.",
    "Distanța există. Conexiunea pare să o ignore.",
    "Raportul confirmă apropierea. Departamentul de obiectivitate nu a participat.",
    "Totul pare suspect de promițător.",
]

SPECIAL_MESSAGES = {
    date(2026, 8, 9): [
        ("EVENIMENT MAJOR", "Răzvan a intrat pe teritoriul României. Alexandra declară că situația este sub control. Sistemul rămâne sceptic."),
        ("PROTOCOL EINDHOVEN", "Decolarea a fost confirmată. Emoțiile nu au respectat procedura de îmbarcare."),
        ("INTRARE ÎN ROMÂNIA", "Distanța fizică scade. Numărul scenariilor mentale refuză să coopereze."),
    ],
    date(2026, 8, 12): [
        ("DEPLASARE INTERNĂ", "Subiectul părăsește Cluj-Napoca. Nivelul de proximitate crește."),
        ("PROTOCOL TRANSILVANIA", "Clujul rămâne în urmă. Ploieștiul începe să pară suspect de aproape."),
        ("TRASEU ACTIV", "S.A.T.A. monitorizează deplasarea și ignoră elegant nerăbdarea."),
    ],
    date(2026, 8, 13): [
        ("STAȚIONARE TÂRGU MUREȘ", "Ultima oprire înainte de Ploiești. Simulările mentale au depășit limita recomandată."),
        ("ULTIMA OPRIRE", "Sistemul recomandă odihnă. Recomandarea are șanse reduse de implementare."),
        ("PROXIMITATE ÎN CREȘTERE", "Orele rămase sunt numărate de mai multe sisteme decât este necesar."),
    ],
    date(2026, 8, 14): [
        ("CONTACT ÎN PLOIEȘTI", "Distanța operațională a fost redusă la zero. Obiectivitatea a părăsit sistemul."),
        ("PLOIEȘTI CONFIRMAT", "Aproape 2000 km au devenit câțiva pași. Algoritmii solicită o pauză."),
        ("CONTACT VIZUAL", "S.A.T.A. suspendă simulările. Realitatea a preluat controlul."),
    ],
    date(2026, 8, 15): [
        ("OPERAȚIUNEA BRAȘOV", "Sistemul suspendă predicțiile. Realitatea urmează să fie observată direct."),
        ("PROTOCOL CARPAȚI", "Echipajul comun este confirmat. Toate concluziile sunt provizorii."),
        ("BRAȘOV ACTIV", "Misiunea continuă fără obiective obligatorii și cu probabilitate ridicată de amintiri bune."),
    ],
}


def _choice_for_session(
    state: MissionState,
    name: str,
    candidates: list,
):
    """Choose once per browser session and avoid immediate repetition."""
    key = f"sata_funny::{state.current_date.isoformat()}::{name}"

    if key in st.session_state:
        return st.session_state[key]

    previous_key = f"sata_funny_previous::{name}"
    previous = st.session_state.get(previous_key)

    available = [item for item in candidates if item != previous]
    if not available:
        available = list(candidates)

    selected = random.SystemRandom().choice(available)
    st.session_state[key] = selected
    st.session_state[previous_key] = selected
    return selected


def _panic_base(state: MissionState) -> int:
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


def _session_number(state: MissionState, name: str, low: int, high: int) -> int:
    key = f"sata_funny_number::{state.current_date.isoformat()}::{name}"
    if key not in st.session_state:
        st.session_state[key] = random.SystemRandom().randint(low, high)
    return int(st.session_state[key])


def render_funny_panel(state: MissionState) -> None:
    special = SPECIAL_MESSAGES.get(state.current_date)
    if special:
        bulletin_title, bulletin_text = _choice_for_session(
            state, "special_bulletin", special
        )
    else:
        bulletin_title = "BULETIN OPERATIV"
        bulletin_text = _choice_for_session(
            state, "general_bulletin", GENERAL_MESSAGES
        )

    phrase, probability_range, phrase_note = _choice_for_session(
        state, "phrase", PHRASE_PROBABILITIES
    )
    probability = _session_number(
        state, "phrase_probability", probability_range[0], probability_range[1]
    )
    recommendation = _choice_for_session(
        state, "recommendation", RECOMMENDATIONS
    )
    summary = _choice_for_session(state, "summary", SUMMARIES)

    panic_base = _panic_base(state)
    panic = max(0, min(100, panic_base + _session_number(state, "panic_jitter", -4, 5)))
    denial = max(0, min(99, panic + _session_number(state, "denial_delta", 3, 10)))
    phone_checks = max(
        3,
        round(panic / 4) + _session_number(state, "phone_jitter", -2, 2),
    )

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
        .summary-card {{
            background:#102436;
            color:#f4f7fa;
            border-radius:16px;
            padding:20px;
            margin-top:14px;
            border:1px solid #294f68;
        }}
        .summary-card .funny-title {{
            color:#68c2ff;
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
                <div class="indicator-label">Probabilitate de panică</div>
                <div class="indicator-value">{panic}%</div>
              </div>
              <div class="indicator-card">
                <div class="indicator-label">Nivel de negare</div>
                <div class="indicator-value">{denial}%</div>
              </div>
              <div class="indicator-card">
                <div class="indicator-label">Verificări estimate ale telefonului</div>
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
          <div class="funny-title">RECOMANDAREA ZILEI</div>
          <div class="funny-main">{recommendation}</div>
        </div>

        <div class="summary-card">
          <div class="funny-title">REZUMATUL S.A.T.A.</div>
          <div class="funny-main">{summary}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
