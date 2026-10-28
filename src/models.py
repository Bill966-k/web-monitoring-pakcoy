"""Loader & inferensi model (LSTM, CNN). TensorFlow di-import malas (lazy)
supaya dasbor tetap jalan walau model/TensorFlow belum tersedia."""
import joblib
import numpy as np
import streamlit as st

from src import config as C
from src.data import daily_means


def lstm_ready() -> bool:
    return C.LSTM_PATH.exists() and C.SCALER_PATH.exists()


def cnn_ready() -> bool:
    return C.CNN_PATH.exists()


@st.cache_resource
def _load_lstm():
    import tensorflow as tf
    return tf.keras.models.load_model(C.LSTM_PATH), joblib.load(C.SCALER_PATH)


@st.cache_resource
def _load_cnn():
    import tensorflow as tf
    return tf.keras.models.load_model(C.CNN_PATH)


def forecast(df, dap):
    """Prediksi HORIZON hari ke depan. Return (array (HORIZON,2) [moist,temp] | None, daily_df)."""
    daily = daily_means(df, dap)
    if len(daily) < C.WINDOW:
        return None, daily
    model, scaler = _load_lstm()
    x = scaler.transform(daily.values).reshape(1, C.WINDOW, 2)
    out = model.predict(x, verbose=0).reshape(C.HORIZON, 2)
    return scaler.inverse_transform(out), daily


def classify(pil_image) -> np.ndarray:
    """Return probabilitas tiap kelas (urutan = C.CLASSES)."""
    cnn = _load_cnn()
    img = pil_image.convert("RGB").resize((C.IMG_SIZE, C.IMG_SIZE))
    arr = np.array(img, dtype="float32")[None]
    return cnn.predict(arr, verbose=0)[0]
