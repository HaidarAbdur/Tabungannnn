# from function import Pemasukan,Pengeluaran,Riwayat
# print('=======Tabungan Kita=======\n')
# def baca_saldo():
#   try:
#    with  open("saldo.txt", "r")as f:
#       return int(f.read())
#   except:
#    return 0
  
# saldo = baca_saldo()
# riwayat = []

# def simpan_saldo(saldo):
#    with open("saldo.txt", "w")as f:
#       f.write(str(saldo))

# def tambah(saldo):
#   with open("saldo.txt", "a")as f:
#     f.write(str(saldo))

# while True:
#     print('Pilih Program!')
#     print('1.Input Pemasukan')
#     print('2.Input Pengeluaran')
#     print('3.Lihat Total')
#     print('4.Reset Total')
#     print('0.Keluar\n')
#     user = input('Silahkan pilih program yang ada: ')

#     if user == '1':
#      saldo += saldo
#      saldo = Pemasukan(saldo,riwayat)
#      tambah(saldo)

     
#     #  with open("saldo.txt","a")as file:
#     #    file.write(str(saldo))

#     elif user == '2':
#      saldo = Pengeluaran(saldo,riwayat)
#      simpan_saldo(saldo)

#     #  with open("saldo.txt","r")as file:
#     #    file.write(str(saldo))
       
#     elif user == '3':
#       Riwayat(riwayat)


#     elif user == '4':
#       reset = input('Apakah ingin mereset saldo anda?[y/n]: ')
#       if reset == 'y':
#        saldo = 0
#        print(f'Saldo berhasil direset Rp.{saldo}')
#       elif reset == 'n':
#        print()

#     elif user == '0':
#      print('Program selesai🙏!')
#      break

#     else:
#      print('Input tidak valid!')
#     continue

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# File untuk menyimpan data (persistent)
DATA_FILE = "tabunganku_data.json"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"saldo": 0, "transaksi": []}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

st.set_page_config(page_title="TabungKu", page_icon="💰", layout="centered")

data = load_data()
saldo = data["saldo"]
transaksi = data["transaksi"]

st.title("💰 TabungKu - Aplikasi Tabunganmu")
st.markdown("### Kelola keuanganmu dengan mudah dan aman")

# Tampilkan saldo
st.metric(label="Saldo Saat Ini", value=f"Rp {saldo:,.0f}")

# Tab navigation
tab1, tab2, tab3 = st.tabs(["➕ Tambah Pemasukan", "➖ Catat Pengeluaran", "📜 Riwayat Transaksi"])

with tab1:
    st.subheader("Tambah Pemasukan")
    jumlah = st.number_input("Jumlah Pemasukan (Rp)", min_value=0, step=1000)
    keterangan = st.text_input("Keterangan (contoh: Gaji, Bonus, dll)")
    if st.button("Tambah ke Saldo"):
        if jumlah > 0 and keterangan:
            saldo += jumlah
            transaksi.append({
                "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "tipe": "Pemasukan",
                "jumlah": jumlah,
                "keterangan": keterangan
            })
            data["saldo"] = saldo
            data["transaksi"] = transaksi
            save_data(data)
            st.success(f"Berhasil menambah Rp {jumlah:,} !")
            st.rerun()
        else:
            st.error("Isi jumlah dan keterangan")

with tab2:
    st.subheader("Catat Pengeluaran")
    jumlah_keluar = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0, step=1000)
    keterangan_keluar = st.text_input("Keterangan Pengeluaran (contoh: Makan, Bensin)")
    if st.button("Kurangi Saldo"):
        if jumlah_keluar > 0 and keterangan_keluar:
            if jumlah_keluar <= saldo:
                saldo -= jumlah_keluar
                transaksi.append({
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "tipe": "Pengeluaran",
                    "jumlah": jumlah_keluar,
                    "keterangan": keterangan_keluar
                })
                data["saldo"] = saldo
                data["transaksi"] = transaksi
                save_data(data)
                st.success(f"Berhasil mengurangi Rp {jumlah_keluar:,} !")
                st.rerun()
            else:
                st.error("Saldo tidak cukup!")
        else:
            st.error("Isi jumlah dan keterangan")

with tab3:
    st.subheader("Riwayat Transaksi")
    if transaksi:
        df = pd.DataFrame(transaksi)
        df["jumlah"] = df.apply(lambda x: f"Rp {x['jumlah']:,.0f}" if x['tipe'] == "Pemasukan" else f"-Rp {x['jumlah']:,.0f}", axis=1)
        st.dataframe(df[["tanggal", "tipe", "jumlah", "keterangan"]], use_container_width=True)
        
        # Ringkasan
        total_masuk = sum(t["jumlah"] for t in transaksi if t["tipe"] == "Pemasukan")
        total_keluar = sum(t["jumlah"] for t in transaksi if t["tipe"] == "Pengeluaran")
        st.info(f"Total Pemasukan: Rp {total_masuk:,.0f} | Total Pengeluaran: Rp {total_keluar:,.0f}")
    else:
        st.info("Belum ada transaksi. Mulai tambah pemasukan atau pengeluaran!")

# Footer
st.caption("Data tersimpan otomatis di file JSON • Bisa diakses kapan saja")
       



 