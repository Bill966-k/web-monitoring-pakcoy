"""Halaman utama — ringkasan sistem. Jalankan: streamlit run app.py"""
import streamlit as st

from src import config as C
from src import history, models
from src.data import fase_dari_dap
from src.growth import load_params
from src.ui import render_sidebar, setup_page

setup_page("Beranda", "🥬")
ctx = render_sidebar()

st.title("🥬 Sistem Monitoring Pertumbuhan Pakcoy")
st.caption("Pantau sensor, prediksi kondisi 4 hari ke depan, dan analisis fase tumbuh dari foto.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Hari tanam (DAP)", ctx.dap)
c2.metric("Kelembaban tanah", f"{ctx.now[C.COL_M]:.0f} %")
c3.metric("Suhu", f"{ctx.now[C.COL_T]:.1f} °C")
c4.metric("Fase (berdasar usia)", fase_dari_dap(ctx.dap))

st.subheader("Menu")
m1, m2, m3 = st.columns(3)
with m1:
    st.page_link("pages/1_Dasbor.py", label="Dasbor Sensor", icon="📊")
    st.page_link("pages/2_Prediksi.py", label="Prediksi 4 Hari (LSTM)", icon="🔮")
with m2:
    st.page_link("pages/3_Analisis_Foto.py", label="Analisis Foto (CNN)", icon="📷")
    st.page_link("pages/4_Ukuran_Tanaman.py", label="Ukuran Tanaman", icon="📏")
with m3:
    st.page_link("pages/5_Histori.py", label="Histori", icon="🗂️")

st.subheader("Status komponen")
_, growth_default = load_params()
st.dataframe(
    {
        "Komponen": ["Data sensor", "Model LSTM + scaler", "Model CNN", "Parameter pertumbuhan"],
        "Status": [
            "✅ Siap" if C.DATA_PATH.exists() else "❌ Tidak ada",
            "✅ Siap" if models.lstm_ready() else "⚠️ Belum ada (taruh di models/)",
            "✅ Siap" if models.cnn_ready() else "⚠️ Belum ada (taruh di models/)",
            "⚠️ Pakai placeholder" if growth_default else "✅ Siap",
        ],
    },
    hide_index=True,
)
st.caption(f"Jumlah data histori tersimpan: {len(history.load())}")
