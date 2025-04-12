# 🚲 Dashboard Analisis Peminjaman Sepeda

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data peminjaman sepeda menggunakan Python dan menyampaikan insight melalui dashboard interaktif yang dibuat dengan Streamlit. Data yang digunakan terdiri dari dua bagian: data harian (`day.csv`) dan data per jam (`hour.csv`). 

Analisis dilakukan mulai dari tahap eksplorasi data, pembersihan data, hingga visualisasi data dan pembuatan dashboard.

---


## 🛠️ Cara Menjalankan Proyek

### 1. Aktifkan Virtual Environment (Opsional)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

### 2. Install Library yang Dibutuhkan
pip install -r requirements.txt

### 3. Jalankan Dashboard Streamlit
streamlit run dashboard/dashboard.py

## 📊 Insight Singkat dari Analisis

    - Peminjaman sepeda cenderung lebih tinggi saat suhu lebih hangat dan kelembapan lebih rendah.

    - Hari kerja memiliki pola jam sibuk di pagi dan sore hari, sementara akhir pekan cenderung ramai di siang hari.

    - Cuaca buruk dan kecepatan angin tinggi dapat menurunkan jumlah peminjaman sepeda secara signifikan.

    - Data menunjukkan tren peningkatan penggunaan sepeda selama tahun yang diamati.

📦 Library yang Digunakan

    - pandas

    - numpy

    - matplotlib

    - seaborn

    - streamlit