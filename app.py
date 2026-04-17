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

DATA_FILE = "tabunganku_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"saldo": 0, "transaksi": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

st.set_page_config(page_title="TabungKu", page_icon="💰", layout="centered")

data = load_data()
saldo = data.get("saldo", 0)
transaksi = data.get("transaksi", [])

st.title("💰 Tabunganku - Aplikasi Tabungan")
st.markdown("### Kelola keuangan dengan mudah diera digital")

# Tampilkan Saldo
st.metric(label="**Saldo Saat Ini**", value=f"Rp {saldo:,.0f}", delta=None)

tab1, tab2, tab3, tab4 = st.tabs(["➕ Pemasukan", "➖ Pengeluaran", "📜 Riwayat", "⚙️ Pengaturan"])

with tab1:
    st.subheader("Tambah Pemasukan")
    jumlah = st.number_input("Jumlah (Rp)", min_value=1000, step=1000)
    ket = st.text_input("Keterangan (contoh: Gaji, THR, dll)")
    if st.button("Tambahkan", type="primary"):
        if jumlah > 0 and ket:
            saldo += jumlah
            transaksi.append({
                "tanggal": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipe": "Pemasukan",
                "jumlah": jumlah,
                "keterangan": ket
            })
            data["saldo"] = saldo
            data["transaksi"] = transaksi
            save_data(data)
            st.success("✅ Pemasukan berhasil ditambahkan!")
            st.rerun()
        else:
            st.warning("Isi jumlah dan keterangan")

with tab2:
    st.subheader("Catat Pengeluaran")
    jumlah_k = st.number_input("Jumlah Pengeluaran (Rp)", min_value=1000, step=1000)
    ket_k = st.text_input("Keterangan Pengeluaran")
    if st.button("Kurangi Saldo", type="primary"):
        if jumlah_k > saldo:
            st.error("❌ Saldo tidak cukup!")
        elif jumlah_k > 0 and ket_k:
            saldo -= jumlah_k
            transaksi.append({
                "tanggal": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipe": "Pengeluaran",
                "jumlah": jumlah_k,
                "keterangan": ket_k
            })
            data["saldo"] = saldo
            data["transaksi"] = transaksi
            save_data(data)
            st.success("✅ Pengeluaran berhasil dicatat!")
            st.rerun()

with tab3:
    st.subheader("Riwayat Transaksi")
    if transaksi:
        df = pd.DataFrame(transaksi)
        df["jumlah"] = df.apply(lambda x: f"Rp {x['jumlah']:,.0f}" if x['tipe']=="Pemasukan" else f"-Rp {x['jumlah']:,.0f}", axis=1)
        st.dataframe(df[["tanggal", "tipe", "jumlah", "keterangan"]], use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Total Pemasukan: Rp {sum(t['jumlah'] for t in transaksi if t['tipe']=='Pemasukan'):,.0f}")
        with col2:
            st.info(f"Total Pengeluaran: Rp {sum(t['jumlah'] for t in transaksi if t['tipe']=='Pengeluaran'):,.0f}")
    else:
        st.info("Belum ada transaksi")

with tab4:
    st.subheader("⚙️ Pengaturan")
    st.warning("⚠️ Fitur ini akan mereset semua data!")
    
    if st.button("🔄 Reset Saldo ke Rp 0", type="secondary"):
        st.session_state.reset_confirm = True

    if st.session_state.get("reset_confirm", False):
        st.error("❗ Apakah Anda yakin ingin reset saldo ke 0 dan menghapus semua riwayat?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Ya, Reset Sekarang"):
                data = {"saldo": 0, "transaksi": []}
                save_data(data)
                st.success("✅ Semua data telah direset!")
                st.session_state.reset_confirm = False
                st.rerun()
        with col_no:
            if st.button("❌ Batal"):
                st.session_state.reset_confirm = False
                st.rerun()

st.caption("• Created by HaidarCode").underline
       



 