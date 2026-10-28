"""Analisis foto pakcoy dengan CNN."""
import pandas as pd
import streamlit as st
from PIL import Image

from src import config as C
from src import growth, history, models
from src.ui import need_model, render_sidebar, setup_page

setup_page("Analisis Foto", "📷")
ctx = render_sidebar()

st.title("📷 Analisis Foto Pakcoy")

if not models.cnn_ready():
    need_model("CNN", "cnn_pakcoy.keras")
    st.stop()

up = st.file_uploader("Upload foto pakcoy", type=["jpg", "jpeg", "png"])
simpan = st.checkbox("Simpan hasil ke histori", value=True)

if up is not None:
    img = Image.open(up).convert("RGB")
    st.image(img, width=320)

    if st.button("Analisis foto", type="primary"):
        prob = models.classify(img)
        k = int(prob.argmax())
        ukuran = growth.estimate(ctx.dap)
        row = {
            "dap": ctx.dap,
            "kelas_cnn": C.CLASSES[k],
            "confidence": round(float(prob[k]), 3),
            "tinggi_cm": round(ukuran["tinggi_cm"], 1),
            "lebar_daun_cm": round(ukuran["lebar_daun_cm"], 1),
            "kelembaban": float(ctx.now[C.COL_M]),
            "suhu": float(ctx.now[C.COL_T]),
        }
        if models.lstm_ready():
            pred, _ = models.forecast(ctx.df, ctx.dap)
            if pred is not None:
                for i in range(C.HORIZON):
                    row[f"pred_kelembaban_h{i+1}"] = round(float(pred[i, 0]), 1)
                    row[f"pred_suhu_h{i+1}"] = round(float(pred[i, 1]), 1)
        if simpan:
            history.append(row)
        st.session_state["hasil_foto"] = (prob, k, simpan)

if "hasil_foto" in st.session_state:
    prob, k, saved = st.session_state["hasil_foto"]
    st.success(f"Fase terdeteksi: **{C.CLASSES[k]}** ({prob[k] * 100:.1f}%)"
               + (" — tersimpan ke histori" if saved else ""))
    st.bar_chart(pd.Series(prob, index=C.CLASSES))
