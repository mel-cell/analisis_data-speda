import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Penyewaan Sepeda",
    page_icon="https://i.pinimg.com/736x/4e/83/f3/4e83f3091159fc587f8de61ded2cacf9.jpg",
    layout="wide"
)

# Load data
data_sepeda = pd.read_csv('dashboard/main_data.csv')
data_sepeda['dteday'] = pd.to_datetime(data_sepeda['dteday'])

# Mapping season dan cuaca
season_labels = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
weather_labels = {
    1: 'Cerah/Clear',
    2: 'Berawan/Mendung',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat/Badai'
}
data_sepeda['season_label'] = data_sepeda['season'].map(season_labels)
data_sepeda['weather_label'] = data_sepeda['weathersit'].map(weather_labels)

# Sidebar filter
with st.sidebar:
    st.title("Filter Data")

    min_date = data_sepeda['dteday'].min().date()
    max_date = data_sepeda['dteday'].max().date()
    date_range = st.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    selected_seasons = st.multiselect(
        "Pilih Musim",
        options=data_sepeda['season_label'].unique(),
        default=data_sepeda['season_label'].unique()
    )

    day_type = st.multiselect(
        "Tipe Hari",
        options=['Hari Kerja', 'Hari Libur'],
        default=['Hari Kerja', 'Hari Libur']
    )

    selected_weather = st.multiselect(
        "Kondisi Cuaca",
        options=data_sepeda['weather_label'].unique(),
        default=data_sepeda['weather_label'].unique()
    )

# Fungsi filter data
def apply_filters(data):
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date)]

    data = data[data['season_label'].isin(selected_seasons)]

    day_map = {'Hari Kerja': 1, 'Hari Libur': 0}
    workingday_values = [day_map[day] for day in day_type]
    data = data[data['workingday'].isin(workingday_values)]

    data = data[data['weather_label'].isin(selected_weather)]

    return data

# Terapkan filter
filtered_data = apply_filters(data_sepeda)

# Tambahan kolom waktu
filtered_data['bulan'] = filtered_data['dteday'].dt.month
filtered_data['tahun'] = filtered_data['dteday'].dt.year
filtered_data['hari'] = filtered_data['dteday'].dt.day
filtered_data['minggu'] = filtered_data['dteday'].dt.isocalendar().week
filtered_data['hari_dalam_minggu'] = filtered_data['dteday'].dt.day_name()  # Bahasa default

# Header utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# Ikhtisar metrik utama
st.header("Ikhtisar Penggunaan Sepeda")
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", int(filtered_data['cnt'].sum()))
col2.metric("Rata-Rata Harian", f"{filtered_data['cnt'].mean():.1f}")
col3.metric("Jumlah Hari Unik", filtered_data['dteday'].nunique())

# Analisis Musim & Cuaca
st.header("Dampak Musim dan Cuaca terhadap Penyewaan")
row1, row2 = st.columns(2)

with row1:
    st.subheader("Penyewaan per Musim")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_data, x='season_label', y='cnt', palette="Set3", ax=ax)
    ax.set_title("Distribusi Penyewaan Berdasarkan Musim")
    st.pyplot(fig)

with row2:
    st.subheader("Penyewaan per Cuaca")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_data, x='weather_label', y='cnt', palette="coolwarm", ax=ax)
    ax.set_title("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
    st.pyplot(fig)

# Analisis Lingkungan
st.header("Korelasi Lingkungan terhadap Penyewaan")
col4, col5 = st.columns(2)

with col4:
    st.subheader("Suhu vs Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_data, x='temp', y='cnt', hue='season_label', alpha=0.7, ax=ax)
    ax.set_title("Hubungan Suhu dengan Jumlah Penyewaan")
    ax.grid(True)
    st.pyplot(fig)

with col5:
    st.subheader("Kelembaban vs Penyewaan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_data, x='hum', y='cnt', alpha=0.6, color='green', ax=ax)
    ax.set_title("Hubungan Kelembaban dengan Jumlah Penyewaan")
    ax.grid(True)
    st.pyplot(fig)

# Kecepatan angin
st.subheader("Kecepatan Angin vs Penyewaan")
fig, ax = plt.subplots(figsize=(12, 5))
sns.scatterplot(data=filtered_data, x='windspeed', y='cnt', alpha=0.6, color='orange', ax=ax)
ax.set_title("Hubungan Kecepatan Angin dengan Jumlah Penyewaan")
ax.grid(True)
st.pyplot(fig)

# Perbandingan hari kerja vs libur
st.header("Perbandingan Penyewaan: Hari Kerja vs Hari Libur")
filtered_data['Tipe Hari'] = filtered_data['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Hari Libur')
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_data, x='Tipe Hari', y='cnt', palette='pastel', ax=ax)
ax.set_title("Distribusi Penyewaan Berdasarkan Tipe Hari")
st.pyplot(fig)

# Tren tahunan
st.header("Tren Penyewaan Sepeda Tahunan")
fig, ax = plt.subplots(figsize=(12, 6))
tren_tahunan = filtered_data.groupby('tahun')['cnt'].sum().reset_index()
sns.barplot(x='tahun', y='cnt', data=tren_tahunan, palette='viridis', ax=ax)
ax.set_title("Total Penyewaan per Tahun")
st.pyplot(fig)

# Tren bulanan
st.header("Tren Penyewaan Sepeda Bulanan")
fig, ax = plt.subplots(figsize=(12, 6))
tren_bulanan = filtered_data.groupby('bulan')['cnt'].sum().reset_index()
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
sns.lineplot(x='bulan', y='cnt', data=tren_bulanan, marker='o', ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(bulan_labels)
ax.set_title("Total Penyewaan per Bulan")
ax.grid(True)
st.pyplot(fig)

# Korelasi antar variabel
st.header("Korelasi antar Variabel")
st.write("Peta korelasi antara variabel lingkungan dan jumlah penyewaan.")
fig, ax = plt.subplots(figsize=(10, 6))
numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
sns.heatmap(filtered_data[numeric_cols].corr(), annot=True, cmap='YlGnBu', ax=ax)
ax.set_title("Heatmap Korelasi")
st.pyplot(fig)

# Distribusi harian
st.header("Distribusi Jumlah Penyewaan Harian")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_data['cnt'], bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title("Distribusi Penyewaan Harian")
st.pyplot(fig)

# Catatan akhir
st.caption("Data dianalisis berdasarkan kombinasi filter waktu, musim, hari, dan cuaca, serta pengaruh suhu, kelembaban, dan kecepatan angin untuk menyesuaikan kebutuhan insight yang fleksibel dan informatif.")
