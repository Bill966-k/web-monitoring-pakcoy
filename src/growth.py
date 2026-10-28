"""Estimasi tinggi & lebar daun berdasarkan usia (kurva logistik)."""
import joblib
import numpy as np

from src import config as C

# Parameter PLACEHOLDER (hmax, k, t0). Ganti dengan hasil fitting data ukur asli (Cell 5).
DEFAULT_PARAMS = {"tinggi": [22.0, 0.20, 20.0], "lebar": [10.0, 0.20, 20.0]}


def logistik(dap, hmax, k, t0):
    return hmax / (1 + np.exp(-k * (np.asarray(dap, dtype=float) - t0)))


def load_params():
    """Return (params, is_default). is_default=True jika file hasil Colab belum ada."""
    if C.GROWTH_PATH.exists():
        return joblib.load(C.GROWTH_PATH), False
    return DEFAULT_PARAMS, True


def estimate(dap: float) -> dict:
    params, _ = load_params()
    return {
        "tinggi_cm": float(logistik(dap, *params["tinggi"])),
        "lebar_daun_cm": float(logistik(dap, *params["lebar"])),
    }
