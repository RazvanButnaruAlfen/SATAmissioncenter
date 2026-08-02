import streamlit as st

from core.sata_memory import record_fear_score, record_prediction

st.set_page_config(page_title="FRICOMETRU.EXE", page_icon="📈", layout="centered")
st.title("📈 FRICOMETRU.EXE")
st.caption("Instrument experimental S.A.T.A. — versiune neomologată 2.3 beta")
st.warning("Acest instrument nu a fost validat științific. Totuși, pare surprinzător de exact.")

fear = st.slider("Cât de frică îmi este de ce se va întâmpla când va veni Răzvan?", 0, 100, 50)
record_fear_score(fear)
st.progress(fear / 100)
st.markdown(f"<div style='font-size:4rem;font-weight:900;text-align:center'>{fear}%</div>", unsafe_allow_html=True)

st.caption(
    "Rezultatul este transmis automat către memoria S.A.T.A. și poate influența "
    "E.M.O.S. și Dosarele Clasificate. Din motive științifice neclare."
)

if fear <= 20:
    st.success("Nivel de calm suspect de ridicat.")
elif fear <= 40:
    st.info("Sistemul detectează o ușoară îngrijorare.")
elif fear <= 60:
    st.warning("Protocolul «Vedem...» a fost activat.")
elif fear <= 80:
    st.warning("Nivel ridicat de scenarii imaginare.")
elif fear < 100:
    st.error("Pericol iminent: verificarea telefonului se intensifică.")
else:
    st.balloons()
    st.error("100% — Răzvan este deja în România.")

predictions = [
    "Alexandra va spune «nu sunt stresată» cu o credibilitate de 3%.",
    "Telefonul va fi verificat de aproximativ 17 ori pe oră.",
    "Planul se va schimba. S.A.T.A. va pretinde că a anticipat asta.",
    "Nivelul de panică va scădea după primele 7 minute. Probabil.",
    "Realitatea va fi mai simplă decât toate scenariile analizate.",
]
if st.button("🔮 Generează predicția", use_container_width=True):
    idx = (st.session_state.get("prediction_index", -1) + 1) % len(predictions)
    st.session_state["prediction_index"] = idx
    prediction = predictions[idx]
    record_prediction(prediction)
    st.info(prediction)

st.page_link("app.py", label="← Înapoi la Mission Center", icon="📡")
