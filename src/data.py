"""Akses data sensor + simulasi live."""
import pandas as pd
import streamlit as st

from src import config as C


@st.cache_data
def load_sensor() -> pd.DataFrame:
    """Baca dataset sensor. Nanti bisa diganti baca dari API/database sensor asli."""
    return pd.read_excel(C.DATA_PATH)


def tick_to_row_idx(df: pd.DataFrame, tick: int) -> int:
    """Mode live: tiap refresh maju 1 baris, lalu berputar ulang dari awal."""
    span = len(df) - C.MIN_IDX
    return C.MIN_IDX + (tick % span)


def dap_to_row_idx(df: pd.DataFrame, dap: int) -> int:
    """Mode manual: ambil pembacaan terakhir (16:00) pada DAP tertentu."""
    return int(df.index[df[C.COL_DAP] == dap][-1])


def daily_means(df: pd.DataFrame, dap: int) -> pd.DataFrame:
    """Rata-rata harian kelembaban & suhu s/d DAP tertentu (maks WINDOW hari terakhir)."""
    sub = df[df[C.COL_DAP] <= dap]
    return sub.groupby(C.COL_DAP)[[C.COL_M, C.COL_T]].mean().tail(C.WINDOW)


def fase_dari_dap(dap: int) -> str:
    """Fase pertumbuhan berdasarkan rentang DAP di dataset (acuan: kolom kriteria)."""
    if dap < 20:
        return "Initial"
    if dap < 30:
        return "Vegetatif"
    if dap < 35:
        return "Pra-Panen"
    return "Siap Panen"
