"""Estimasi tinggi & lebar daun berdasarkan usia tanaman."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src import growth
from src.ui import render_sidebar, setup_page

setup_page("Ukuran Tanaman", "📏")
ctx = render_sidebar()

st.title("📏 Ukuran Tanaman Berdasarkan Usia")

params, is_default = growth.load_params()
if is_default:
    st.warning("Memakai parameter **placeholder**. Jalankan Cell 5 di Colab dengan data ukur asli, "
               "lalu taruh `growth_params.pkl` di folder `models/`.")

dap = st.slider("Usia tanaman (DAP)", 10, 45, min(max(ctx.dap, 10), 45))
u = growth.estimate(dap)
a, b = st.columns(2)
a.metric("Tinggi tanaman", f"{u['tinggi_cm']:.1f} cm")
b.metric("Lebar daun", f"{u['lebar_daun_cm']:.1f} cm")

xs = np.arange(10, 46)
fig = go.Figure()
fig.add_trace(go.Scatter(x=xs, y=growth.logistik(xs, *params["tinggi"]), name="Tinggi (cm)"))
fig.add_trace(go.Scatter(x=xs, y=growth.logistik(xs, *params["lebar"]), name="Lebar daun (cm)"))
fig.add_vline(x=dap, line_dash="dash")
fig.update_layout(xaxis_title="DAP", yaxis_title="cm", height=350, margin=dict(t=20, b=10))
st.plotly_chart(fig)
st.caption("Estimasi dari kurva logistik hasil fitting data ukur, bukan pengukuran langsung.")
