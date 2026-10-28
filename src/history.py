"""Penyimpanan histori hasil analisis (CSV)."""
from datetime import datetime

import pandas as pd

from src import config as C


def append(row: dict) -> None:
    row = {"waktu": datetime.now().isoformat(timespec="seconds"), **row}
    pd.DataFrame([row]).to_csv(
        C.HISTORY_PATH, mode="a", header=not C.HISTORY_PATH.exists(), index=False
    )


def load() -> pd.DataFrame:
    if not C.HISTORY_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(C.HISTORY_PATH)
