"""Dasbor: grafik kelembaban tanah & suhu yang bergerak (live)."""
import plotly.graph_objects as go
import streamlit as st

from src import config as C
from src.data import fase_dari_dap
from src.ui import render_sidebar, setup_page

setup_page("Dasbor", "📊")
ctx = render_sidebar(autorefresh=True)

st.title("📊 Dasbor Sensor")
now, df = ctx.now, ctx.df

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Kelembaban tanah", f"{now[C.COL_M]:.0f} %")
c2.metric("Suhu", f"{now[C.COL_T]:.1f} °C")
c3.metric("Kondisi tanah", str(now[C.COL_COND]))
c4.metric("Fase", fase_dari_dap(ctx.dap))
c5.metric("Waktu", f"DAP {ctx.dap} · {now[C.COL_TIME]}")

view = df.iloc[max(0, ctx.idx - C.CHART_POINTS + 1): ctx.idx + 1]
x = "D" + view[C.COL_DAP].astype(str) + " " + view[C.COL_TIME].astype(str)


def line_chart(col, title, color, unit):
    lo, hi = df[col].min(), df[col].max()
    pad = max((hi - lo) * 0.15, 1)
    fig = go.Figure(go.Scatter(x=x, y=view[col], mode="lines+markers", line=dict(color=color)))
    fig.update_layout(
        title=title, height=320, margin=dict(t=40, b=10, l=10, r=10),
        yaxis=dict(range=[lo - pad, hi + pad], title=unit), xaxis=dict(showticklabels=False),
    )
    return fig


g1, g2 = st.columns(2)
g1.plotly_chart(line_chart(C.COL_M, "Kelembaban Tanah", "#2e86de", "%"))
g2.plotly_chart(line_chart(C.COL_T, "Suhu", "#e67e22", "°C"))

st.caption("Mode live memutar ulang dataset sebagai simulasi sensor. Matikan di sidebar untuk memilih hari manual.")
