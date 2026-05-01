import streamlit as st
import pandas as pd
from datetime import datetime
import requests

API_URL = "http://localhost:8000/transaksi"

def load_data():
    try:
        response = requests.get(API_URL)
        
        if response.status_code ==200:
            data = response.json()
            return data["saldo"], data["transaksi"]
        else:
            st.error(f"❌ Gagal mengambil data")
            return 0, []

    except requests.exceptions.RequestException as err:
        st.error(f"❌ Tidak dapat terhubung ke API {err}")

        st.info("Pastikan server FastAPI (uvicorn) berjalan di terminal")
        return 0, []

    transaksi = []
    saldo = 0

    for row in rows:
        t = {
            "tanggal":row["tanggal"],
            "tipe":row["tipe"],
            "jumlah":row["jumlah"],
            "keterangan":row["keterangan"]
        }
        transaksi.append(t)

        if t["tipe"]=="Pemasukan":
            saldo += t["jumlah"]
        else:
            saldo -= t["jumlah"]

    return saldo, transaksi

st.set_page_config(page_title="TabungKu", page_icon="💰", layout="centered")

saldo,transaksi = load_data()

st.title("💰 Tabunganku - Aplikasi Tabungan")
st.markdown("### Kelola keuangan dengan mudah dan aman diera digital")

# Tampilkan Saldo
st.metric(label="**Saldo Saat Ini**", value=f"Rp {saldo:,.0f}", delta=None)

tab1, tab2, tab3, tab4 = st.tabs(["➕ Pemasukan", "➖ Pengeluaran", "📜 Riwayat", "⚙️ Pengaturan"])

with tab1:
    st.subheader("Tambah Pemasukan")
    jumlah = st.number_input("Jumlah (Rp)", min_value=1000, step=1000)
    ket = st.text_input("Keterangan (contoh: Gaji, THR, dll)")
    if st.button("Tambahkan", type="primary"):
        if jumlah > 0 and ket:
          try:
            paket_data = {
                "tipe":"Pemasukan",
                "jumlah":jumlah,
                "keterangan":ket
            }
            response = requests.post(API_URL, json=paket_data)

            if response.status_code == 200:
                st.success("✅ Berhasil ditambahkan!")
                st.rerun()
            else:
                st.error("Gagal menambahkan data")
        
          except requests.exceptions.RequestException as err:
            st.error(f"Gagal terhubung ke API")
        else:
            st.warning("Isi jumlah dan keterangan")

with tab2:
    st.subheader("Catat Pengeluaran")
    jumlah_k = st.number_input("Jumlah Pengeluaran (Rp)", min_value=1000, step=1000)
    ket_k = st.text_input("Keterangan Pengeluaran")
    if st.button("Kurangi Saldo", type="primary"):
        if jumlah_k > saldo:
            st.error("Saldo tidak cukup")
        elif jumlah_k > 0 and ket_k:
          try:
            paket_data = {
                "tipe":"Pengeluaran",
                "jumlah":jumlah_k,
                "keterangan":ket_k
            }
            response = requests.post(API_URL, json=paket_data)

            if response.status_code == 200:
                st.success("✅ Berhasil ditambahkan!")
                st.rerun()
            else:
                st.error("Gagal menambahkan data")

          except requests.exceptions.RequestException as err:
            st.error(f"Gagal terhubung ke API")
    else:
        st.warning("Isi jumlah dan keterangan")
        
        

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
                try:    
                    response = requests.delete(API_URL)
                    if response.status_code == 200:
                        st.success("✅ Semua data telah direset!")
                        st.session_state.reset_confirm = False
                        st.rerun()
                except requests.exceptions.RequestException as err:
                    st.error(f"Gagal terhubung ke API")

        with col_no:
            if st.button("❌ Batal"):
                st.session_state.reset_confirm = False
                st.rerun()

st.caption("• Created by HaidarCode")
       



 