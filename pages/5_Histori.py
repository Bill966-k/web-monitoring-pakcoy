"""Histori hasil analisis."""
import streamlit as st

from src import history
from src.ui import render_sidebar, setup_page

setup_page("Histori", "🗂️")
render_sidebar()

st.title("🗂️ Histori Analisis")

h = history.load()
if h.empty:
    st.info("Belum ada histori. Lakukan analisis di halaman **Analisis Foto** dulu.")
    st.stop()

c1, c2 = st.columns(2)
c1.metric("Total analisis", len(h))
c2.metric("Analisis terakhir", str(h["waktu"].iloc[-1]))

kelas = st.multiselect("Filter fase", sorted(h["kelas_cnn"].unique()))
view = h[h["kelas_cnn"].isin(kelas)] if kelas else h
st.dataframe(view.iloc[::-1], hide_index=True)
st.download_button("Download CSV", view.to_csv(index=False), "histori_pakcoy.csv", "text/csv")
