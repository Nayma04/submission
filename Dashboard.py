import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
st.write(
    """
    # Dashboard Projek Akhir
    Analisis data dengan Phyton
    """
)

day_df = pd.read_csv("penyewaan_sepeda.csv")

def create_BarPenyewaSepeda_SetiapMusim_df(df):
    plt.figure(figsize=(8,5))
    sns.barplot(x="season", y="cnt", data = day_df, estimator=sum)
    plt.xticks(ticks=[0, 1, 2, 3], labels=["Dingin", "Panas", "Gugur", "Semi"])
    plt.xlabel("Musim")
    plt.ylabel("Total Penyewaan Sepeda")
    plt.title("Total Penyewaan Sepeda di Setiap Musim")
    plt.show()

def create_BoxPenyewaSepeda_SetiapMusim_df(df):
    plt.figure(figsize=(8,5))
    sns.boxplot(x="season", y="cnt", data=day_df)
    plt.xticks(ticks=[0, 1, 2, 3], labels=["Dingin", "Panas", "Gugur", "Semi"])
    plt.xlabel("Musim")
    plt.ylabel("Penyewaan Sepeda")
    plt.title("Distribusi Penyewaan Sepeda di Setiap Musim")
    plt.show()

def create_ScatterWindspeed_df(df):
    plt.figure(figsize=(8,5))
    sns.scatterplot(
    x="windspeed",
    y="cnt",
    hue="year",
    data=day_df,
    alpha=0.5,
    palette={0: "red", 1: "blue"}  # 2011 = merah, 2012 = biru
    )
    # Tambahkan label dan judul
    plt.xlabel("Kecepatan Angin")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    plt.title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda (Berdasarkan Tahun)")
    # Perbaiki label legenda agar sesuai dengan tahun
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles, ["2011", "2012"], title="Tahun")
    plt.show()

def create_HeatmapWindspeed_df(df):
    working_day_df = df[df['workingday'] == 1]
    bins = [0.02, 0.13, 0.23, 0.50]
    labels = ["Rendah", "Sedang", "Kencang"]
    working_day_df.loc[:, "wind_category"] = pd.cut(working_day_df["windspeed"], bins=bins, labels=labels).astype("category")
    wind_avg_rentals = working_day_df.groupby("wind_category")["cnt"].mean()
    selected_vars = ["temp", "atemp", "hum", "windspeed", "cnt"]
    corr_matrix = day_df[selected_vars].corr()
    plt.figure(figsize=(6,4))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Heatmap Korelasi (temp, atemp, hum, windspeed, cnt)")
    plt.show()

def create_StackedHoliday_df(df):
    # Memisahkan data untuk hari libur dan hari kerja
    holiday_only = day_df[day_df["holiday"] == 1]
    working_day_only = day_df[day_df["holiday"] == 0]
    # Menghitung total penyewaan sepeda untuk hari libur
    total_casual_holiday = holiday_only["casual"].sum()
    total_registered_holiday = holiday_only["registered"].sum()
    # Menghitung total penyewaan sepeda untuk hari kerja
    total_casual_working = working_day_only["casual"].sum()
    total_registered_working = working_day_only["registered"].sum()
    # Membuat dua subplot untuk hari libur dan hari kerja
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    # Stacked Bar Chart untuk Hari Libur
    ax[0].bar("Hari Libur", total_casual_holiday, label="Casual", color="red")
    ax[0].bar("Hari Libur", total_registered_holiday, bottom=total_casual_holiday, label="Registered", color="blue")
    ax[0].set_ylabel("Total Penyewaan Sepeda")
    ax[0].set_title("Penyewaan Sepeda pada Hari Libur")
    ax[0].legend()
    # Stacked Bar Chart untuk Hari Kerja
    ax[1].bar("Hari Kerja", total_casual_working, label="Casual", color="red")
    ax[1].bar("Hari Kerja", total_registered_working, bottom=total_casual_working, label="Registered", color="blue")
    ax[1].set_ylabel("Total Penyewaan Sepeda")
    ax[1].set_title("Penyewaan Sepeda pada Hari Kerja")
    ax[1].legend()
    plt.show()

def create_ViolinHoliday_df(df):
    # Memisahkan data untuk hari libur dan hari kerja
    holiday_only = day_df[day_df["holiday"] == 1]
    working_day_only = day_df[day_df["holiday"] == 0]
    # Mengubah data menjadi format yang sesuai untuk seaborn (Hari Libur)
    violin_holiday = holiday_only.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                                   var_name="User Type", value_name="Total Penyewaan")
    # Mengubah data menjadi format yang sesuai untuk seaborn (Hari Kerja)
    violin_working = working_day_only.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                                       var_name="User Type", value_name="Total Penyewaan")
    # Membuat dua subplot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    # Violin Plot untuk Hari Libur
    sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_holiday,
               palette={"casual": "red", "registered": "blue"}, ax=ax[0])
    ax[0].set_title("Distribusi Penyewaan Sepeda pada Hari Libur")
    ax[0].set_xlabel("Jenis Pengguna")
    ax[0].set_ylabel("Jumlah Penyewaan Sepeda")
    # Violin Plot untuk Hari Kerja
    sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_working,
               palette={"casual": "red", "registered": "blue"}, ax=ax[1])
    ax[1].set_title("Distribusi Penyewaan Sepeda pada Hari Kerja")
    ax[1].set_xlabel("Jenis Pengguna")
    ax[1].set_ylabel("Jumlah Penyewaan Sepeda")
    plt.tight_layout()
    plt.show()

days_df = pd.read_csv(r"C:/Users/Lenovo/Documents/Kuliah/Semester 6/Dicoding/penyewaan_sepeda.csv") 
 
with st.sidebar:
    st.header("Penyewaan Sepeda")
    
    BarPenyewaSepeda_SetiapMusim_df = create_BarPenyewaSepeda_SetiapMusim_df
    BoxPenyewaSepeda_SetiapMusim_df = create_BoxPenyewaSepeda_SetiapMusim_df
    ScatterWindspeed_df = create_ScatterWindspeed_df
    BarWindspeed_df = create_HeatmapWindspeed_df
    StackeHoliday_df = create_StackedHoliday_df
    ViolinHoliday_df = create_ViolinHoliday_df
    
    # Data total penyewaan berdasarkan musim
    season_rentals = {
    "Musim Dingin": 471348,
    "Musim Panas": 918589,
    "Musim Gugur": 1061129,
    "Musim Semi": 841613
    }
    # Membuat filter dropdown untuk memilih musim
    selected_season = st.selectbox("Pilih Musim:", list(season_rentals.keys()))
     # Membuat filter hari libur atau bukan
    holiday_option = st.radio("Pilih Jenis Hari:", ["Hari Libur", "Hari Biasa"])
    # Mengatur filter berdasarkan pilihan pengguna
    if holiday_option == "Hari Libur":
        filtered_df = days_df[days_df["holiday"] == 1]
    else:
        filtered_df = days_df[days_df["holiday"] == 0]

st.header("🚲 Dashboard Bike Sharing Dataset")
st.subheader("📅 Season")

# Menampilkan jumlah penyewaan sesuai musim yang dipilih
st.metric(label=f"Total Penyewaan - {selected_season}", value=season_rentals[selected_season])
    

# Menghitung total penyewaan sepeda di setiap musim
season_df = days_df.groupby("season")["cnt"].sum().reset_index()

# Mapping nama musim
season_names = {1: "Musim Dingin", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Semi"}
season_df["season_name"] = season_df["season"].map(season_names)

# Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader("📊 Penyewaan Sepeda di Setiap Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_df["season_name"], y=season_df["cnt"], palette="viridis", ax=ax)
plt.xlabel("Musim")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Jumlah Penyewaan Sepeda di Setiap Musim")
st.pyplot(fig)

st.subheader("📊 Boxplot Penyewaan Sepeda Berdasarkan Musim")
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(8, 5))

# Membuat Boxplot
sns.boxplot(x="season", y="cnt", data=day_df, ax=ax, palette="Set2")

# Menambahkan label dan judul
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Distribusi Penyewaan Sepeda di Setiap Musim")

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Header
st.subheader("🌬 Windspeed Analysis")

# Kategorisasi Windspeed menjadi Rendah, Sedang, dan Tinggi
bins = [0.13, 0.18, 0.23, 0.30]  
labels = ["Rendah", "Sedang", "Tinggi"]
days_df["windspeed_category"] = pd.cut(days_df["windspeed"], bins=bins, labels=labels)

# *Scatter Plot Windspeed vs Penyewaan Sepeda*
st.subheader("📈 Scatter Plot Windspeed")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=days_df["windspeed"], y=days_df["cnt"], alpha=0.5, ax=ax)
plt.xlabel("Windspeed")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Hubungan Windspeed dan Penyewaan Sepeda")
st.pyplot(fig)
# *Bar Chart Windspeed dengan Kategori*
st.subheader("📊 Bar Chart Windspeed (Kategori)")
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(8, 5))
# Membuat bar chart
sns.barplot(x=days_df["windspeed_category"], y=days_df["windspeed"], ax=ax, palette="Set2")
# Menambahkan label
plt.xlabel("Kategori Windspeed")
plt.ylabel("Rata-rata Windspeed")
plt.title("Rata-rata Windspeed Berdasarkan Kategori")
# Menampilkan plot di Streamlit
st.pyplot(fig)

st.subheader("🎻 Distribusi Penyewaan Sepeda")
# Menampilkan subheader berdasarkan pilihan
st.subheader(f"📊 Analisis Penyewaan Sepeda pada {holiday_option}")

# Menghitung total penyewaan
casual_counts = filtered_df["casual"].sum()
registered_counts = filtered_df["registered"].sum()

# Membuat visualisasi Stacked Bar Chart
fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(holiday_option, casual_counts, label="Casual", color="red")
ax.bar(holiday_option, registered_counts, bottom=casual_counts, label="Registered", color="blue")

# Menambahkan label dan judul
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title(f"Perbandingan Penyewaan Sepeda pada {holiday_option}")
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# VIOLIN CHART 
# Transformasi Data untuk Violin Plot
violin_df = filtered_df.melt(id_vars=["holiday"], value_vars=["casual", "registered"],
                             var_name="User Type", value_name="Total Penyewaan")


# Membuat Violin Chart
fig, ax = plt.subplots(figsize=(6, 5))
sns.violinplot(x="User Type", y="Total Penyewaan", data=violin_df, palette={"casual": "red", "registered": "blue"}, ax=ax)
st.subheader(f"📊 Analisis Penyewaan Sepeda pada {holiday_option}")

# Menambahkan judul dan label
ax.set_title("Distribusi Penyewaan Sepeda pada Hari Libur")
ax.set_xlabel("Jenis Pengguna")
ax.set_ylabel("Jumlah Penyewaan Sepeda")

# Menampilkan plot di Streamlit
st.pyplot(fig)
