import calendar
from datetime import date

import pandas as pd
import streamlit as st

import db
from content import CATEGORIES, SIGNS
from engine import MONTHS_ES, ExhaustedError, generate_month
from exporter import build_xlsx, filename

st.set_page_config(page_title="Horóscopo Mensual", page_icon="✨", layout="wide")

st.markdown(
    """
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
.hero {background: linear-gradient(135deg,#3b2a78 0%,#6b3fa0 55%,#c9a2ff 100%);
  border-radius: 20px; padding: 2rem 2.2rem; margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px rgba(107,63,160,.35);}
.hero h1 {margin:0; color:#fff; font-size: 2.2rem;}
.hero p {margin:.3rem 0 0; color:#efe6ff; font-size:1.05rem;}
.card {background:#1a1433; border:1px solid #2e2457; border-radius:16px;
  padding:1rem 1.2rem; margin-bottom:.8rem;}
.card h4 {margin:0 0 .2rem;}
.badge {display:inline-block; padding:.15rem .7rem; border-radius:999px;
  font-size:.78rem; font-weight:600;}
.pub {background:#1f6f4a; color:#d6ffe9;} .draft {background:#3a3366; color:#d9d0ff;}
.meta {color:#a99bd6; font-size:.88rem;}
div.stButton > button, div.stDownloadButton > button {border-radius:12px; font-weight:600;}
</style>
<div class="hero"><h1>✨ Horóscopo Mensual</h1>
<p>Genera, versiona y publica pronósticos únicos para los 12 signos, todos los días del mes.</p></div>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False, max_entries=20)
def xlsx_for(hid):
    return build_xlsx(db.get_entries(hid))


def fmt(h):
    return f"{MONTHS_ES[h['month'] - 1]} {h['year']} · V{h['version']}"


tab_gen, tab_lib, tab_view = st.tabs(["✨ Generar", "📚 Versiones", "🔎 Vista previa"])

# ---------------------------------------------------------------- Generar
with tab_gen:
    today = date.today()
    nxt = today.month % 12 + 1
    c1, c2, c3 = st.columns([2, 1, 1.4])
    month = c1.selectbox("Mes", range(1, 13), index=nxt - 1, format_func=lambda m: MONTHS_ES[m - 1])
    year = c2.number_input("Año", 2020, 2100, today.year + (1 if today.month == 12 else 0), step=1)
    c3.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
    go = c3.button("✨ Generar horóscopo", type="primary", width="stretch")
    days = calendar.monthrange(int(year), month)[1]
    st.caption(
        f"Se generarán {days} días × 12 signos × 4 categorías = {days * 48} pronósticos únicos, "
        "distintos a todo lo ya guardado. Cada generación crea una nueva versión."
    )
    if go:
        try:
            with st.spinner("Escribiendo las estrellas…"):
                entries = generate_month(int(year), month, db.used_texts())
                hid = db.save_horoscope(int(year), month, entries)
            st.session_state["last_id"] = hid
        except ExhaustedError as e:
            st.error(str(e))
    hid = st.session_state.get("last_id")
    h = db.get_horoscope(hid) if hid else None
    if h:
        st.success(f"Listo: {fmt(h)} guardado en la base de datos.")
        st.download_button(
            "⬇️ Descargar Excel", xlsx_for(h["id"]), filename(h["year"], h["month"], h["version"]),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_new",
        )

# ---------------------------------------------------------------- Versiones
with tab_lib:
    items = db.list_horoscopes()
    if not items:
        st.info("Todavía no hay horóscopos generados.")
    for h in items:
        with st.container():
            st.markdown(
                f"<div class='card'><h4>{MONTHS_ES[h['month'] - 1]} {h['year']} · V{h['version']} "
                f"<span class='badge {'pub' if h['published'] else 'draft'}'>"
                f"{'Publicado' if h['published'] else 'Borrador'}</span></h4>"
                f"<span class='meta'>Creado: {h['created_at']}</span></div>",
                unsafe_allow_html=True,
            )
            a, b, c = st.columns([1.2, 1.6, 1.2])
            pub = a.checkbox("Publicado", value=bool(h["published"]), key=f"pub{h['id']}")
            if pub != bool(h["published"]):
                db.set_published(h["id"], pub)
                st.rerun()
            b.download_button(
                "⬇️ Descargar Excel", xlsx_for(h["id"]), filename(h["year"], h["month"], h["version"]),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key=f"dl{h['id']}",
            )
            if st.session_state.get("confirm_del") == h["id"]:
                if c.button("Confirmar eliminación", key=f"cf{h['id']}", type="primary"):
                    db.delete_horoscope(h["id"])
                    xlsx_for.clear()
                    st.session_state.pop("confirm_del")
                    st.rerun()
            elif c.button("🗑️ Eliminar", key=f"del{h['id']}"):
                st.session_state["confirm_del"] = h["id"]
                st.rerun()

# ---------------------------------------------------------------- Vista previa
with tab_view:
    items = db.list_horoscopes()
    if not items:
        st.info("Genera un horóscopo para verlo aquí.")
    else:
        v1, v2 = st.columns(2)
        h = v1.selectbox("Versión", items, format_func=fmt)
        sign = v2.selectbox("Signo", SIGNS)
        rows = [r for r in db.get_entries(h["id"]) if r["sign"] == sign]
        df = pd.DataFrame(rows).pivot(index="day", columns="category", values="text")[CATEGORIES]
        df.index = [date.fromisoformat(d).strftime("%d/%m/%Y") for d in df.index]
        df.index.name = "Fecha"
        st.dataframe(df, width="stretch", height=600)
