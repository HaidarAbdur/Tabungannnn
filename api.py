from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from datetime import datetime


# membuat server api
app = FastAPI(title="API Tabungan")

# login database mysql
DB_CONFIG = {
    "host": "localhost",
    "user" : "root",
    "password" : "",
    "database": "db_tabungan"
}

# function koneksi database
def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500,detail=f"Koneksi ke database error!")

# struktur data
class TransaksiRequest(BaseModel):
    tipe: str
    jumlah: int
    keterangan: str

# endpoint
@app.get("/transaksi")
def get_transaksi():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM transaksi")
        rows = cursor.fetchall()
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

        return {"saldo":saldo, "transaksi":transaksi}

    finally:
        cursor.close()
        conn.close()

# endpoint tambah transaksi
@app.post("/transaksi")
def tambah_transaksi(req: TransaksiRequest):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO transaksi (tanggal, tipe, jumlah, keterangan) VALUES (%s, %s, %s, %s)"
        val = (tanggal , req.tipe, req.jumlah, req.keterangan)
        cursor.execute(sql, val)
        conn.commit()

        return {"message": "Transaksi berhasil ditambahkan!"}        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Gagal menambahkan transaksi")
    
    finally:
        cursor.close()
        conn.close()

# Endpoint reset/delete
@app.delete("/transaksi")
def reset_transaksi(): 
    conn = get_connection()
    cursor = conn.cursor()
    

    try:
        cursor.execute("DELETE FROM transaksi")
        conn.commit()

        return{"message":"Semua data transaksi berhasil dihapus"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Gagal menghapus data")

    finally:
        cursor.close()
        conn.close()