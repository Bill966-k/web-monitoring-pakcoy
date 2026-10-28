"""Konfigurasi terpusat: path file, hyperparameter, nama kolom."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Path file ---------------------------------------------------------
DATA_PATH = ROOT / "data" / "new_Dataset_Pakcoy.xlsx"
HISTORY_PATH = ROOT / "data" / "histori.csv"

MODEL_DIR = ROOT / "models"
LSTM_PATH = MODEL_DIR / "lstm_pakcoy.keras"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
CNN_PATH = MODEL_DIR / "cnn_pakcoy.keras"
GROWTH_PATH = MODEL_DIR / "growth_params.pkl"

# --- Hyperparameter (HARUS sama dengan yang dipakai di Colab) ----------
WINDOW = 14      # jumlah hari input LSTM
HORIZON = 4      # jumlah hari prediksi
IMG_SIZE = 224   # ukuran input CNN
CLASSES = ["Masa Pertumbuhan", "Mendekati Panen", "Siap Panen"]

# --- Nama kolom dataset ------------------------------------------------
COL_DAP = "DAP"
COL_TIME = "Time"
COL_M = "Soil Moisture (%)"
COL_T = "Temperature (°C)"
COL_COND = "Soil Condition"

# --- Dasbor ------------------------------------------------------------
CHART_POINTS = 60                          # titik yang ditampilkan di grafik live
READINGS_PER_DAY = 3                       # 08:00, 12:00, 16:00
MIN_IDX = WINDOW * READINGS_PER_DAY - 1    # indeks minimal supaya LSTM punya 14 hari
