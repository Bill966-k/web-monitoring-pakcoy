"""Komponen UI bersama: setup halaman + sidebar (dipakai semua halaman)."""
from dataclasses import dataclass

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src import config as C
from src.data import dap_to_row_idx, load_sensor, tick_to_row_idx


@dataclass
class Context:
    df: pd.DataFrame
    idx: int
    now: pd.Series
    dap: int
    live: bool


def setup_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} · Monitoring Pakcoy", page_icon=icon, layout="wide")


def render_sidebar(autorefresh: bool = False) -> Context:
    """Render sidebar & hitung posisi data saat ini.
    autorefresh=True hanya untuk halaman Dasbor (supaya halaman lain tidak refresh terus)."""
    df = load_sensor()
    st.sidebar.title("🥬 Monitoring Pakcoy")
    live = st.sidebar.checkbox("Mode live (simulasi sensor)", value=True, key="live")

    if live:
        interval = st.sidebar.slider("Interval refresh (detik)", 1, 10, 3, key="interval")
        if autorefresh:
            st.session_state["tick"] = st_autorefresh(interval=interval * 1000, key="tick_refresh")
        idx = tick_to_row_idx(df, st.session_state.get("tick", 0))
    else:
        dap_min = int(df[C.COL_DAP].min()) + C.WINDOW
        dap_max = int(df[C.COL_DAP].max())
        dap_sel = st.sidebar.slider("Posisi data (DAP)", dap_min, dap_max, 40, key="dap_manual")
        idx = dap_to_row_idx(df, dap_sel)

    now = df.iloc[idx]
    dap = int(now[C.COL_DAP])
    st.sidebar.metric("Hari tanam (DAP)", dap)
    st.sidebar.caption("Data sensor diputar ulang dari dataset sebagai simulasi.")
    return Context(df=df, idx=idx, now=now, dap=dap, live=live)


def need_model(name: str, filenames: str) -> None:
    st.warning(
        f"Model **{name}** belum ada. Taruh file `{filenames}` di folder `models/` "
        "(hasil training dari Google Colab), lalu refresh halaman."
    )
