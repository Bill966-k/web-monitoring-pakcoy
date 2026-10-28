"""Prediksi kelembaban & suhu 4 hari ke depan (LSTM)."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import config as C
from src import models
from src.ui import need_model, render_sidebar, setup_page

setup_page("Prediksi", "🔮")
ctx = render_sidebar()

st.title("🔮 Prediksi 4 Hari ke Depan")

if not models.lstm_ready():
    need_model("LSTM", "lstm_pakcoy.keras + scaler.pkl")
    st.stop()

pred, daily = models.forecast(ctx.df, ctx.dap)
if pred is None:
    st.warning(f"Data belum cukup (butuh {C.WINDOW} hari).")
    st.stop()

hari = [f"H+{i}" for i in range(1, C.HORIZON + 1)]
st.dataframe(
    pd.DataFrame({"Hari": hari, "Kelembaban (%)": pred[:, 0].round(1), "Suhu (°C)": pred[:, 1].round(1)}),
    hide_index=True,
)


def chart(col_idx, col_name, title, color):
    hist_x = [f"D{d}" for d in daily.index]
    fut_x = [f"D{ctx.dap + i}" for i in range(1, C.HORIZON + 1)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_x, y=daily[col_name], name="Aktual (rata-rata harian)",
                             line=dict(color=color)))
    # sambungkan titik terakhir aktual ke prediksi supaya garis nyambung
    fig.add_trace(go.Scatter(x=[hist_x[-1]] + fut_x, y=[daily[col_name].iloc[-1]] + list(pred[:, col_idx]),
                             name="Prediksi", line=dict(color=color, dash="dash")))
    fig.update_layout(title=title, height=320, margin=dict(t=40, b=10, l=10, r=10))
    return fig


g1, g2 = st.columns(2)
g1.plotly_chart(chart(0, C.COL_M, "Kelembaban Tanah (%)", "#2e86de"))
g2.plotly_chart(chart(1, C.COL_T, "Suhu (°C)", "#e67e22"))
st.caption(f"Input: rata-rata harian {C.WINDOW} hari terakhir sampai DAP {ctx.dap}.")
