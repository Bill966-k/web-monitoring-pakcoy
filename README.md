# 🥬 Sistem Monitoring Pertumbuhan Pakcoy

Website monitoring berbasis Streamlit: dasbor sensor live, prediksi LSTM 4 hari,
klasifikasi fase dari foto (CNN), estimasi ukuran tanaman, dan histori.

## Struktur
```
pakcoy-web/
├── app.py                  # Beranda (ringkasan + status komponen)
├── pages/
│   ├── 1_Dasbor.py         # grafik kelembaban & suhu live
│   ├── 2_Prediksi.py       # LSTM: prediksi 4 hari
│   ├── 3_Analisis_Foto.py  # CNN: klasifikasi fase dari foto
│   ├── 4_Ukuran_Tanaman.py # tinggi & lebar daun vs usia
│   └── 5_Histori.py        # riwayat analisis + download CSV
├── src/
│   ├── config.py           # path, hyperparameter, nama kolom
│   ├── data.py             # load dataset, simulasi live
│   ├── models.py           # load & inferensi LSTM/CNN
│   ├── growth.py           # kurva pertumbuhan
│   ├── history.py          # simpan/baca histori
│   └── ui.py               # sidebar & komponen bersama
├── data/                   # dataset sensor + histori.csv
├── models/                 # model hasil Colab
├── .streamlit/config.toml
└── requirements.txt
```

## Menjalankan
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Dasbor langsung jalan tanpa model. Halaman Prediksi & Foto butuh file di `models/`.

## Ambil model dari Colab
```python
from google.colab import files
for f in ["lstm_pakcoy.keras", "scaler.pkl", "cnn_pakcoy.keras", "growth_params.pkl"]:
    files.download(f)
```

## Catatan
- `WINDOW`, `HORIZON`, `IMG_SIZE` di `src/config.py` harus sama dengan di Colab.
- Versi TensorFlow lokal sebaiknya sama dengan di Colab.
- Sensor masih simulasi dari dataset. Untuk sensor asli, ganti `load_sensor()` di `src/data.py`.
