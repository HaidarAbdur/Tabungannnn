def Pemasukan(saldo):
 while True:
       try:
        saldo = 0
        saldo = int(input('Masukan uang pemasukan: '))
        if saldo <= 0:
            print('Uang harus lebih dari 0')
            continue
        elif saldo >= 0:
            print(f'Saldo berhasil ditambahkan sebesar Rp.{saldo}')
       except ValueError:
           print('Input harus berupa angka')
           continue
       saldo + saldo
       break
 return saldo
 
def Pengeluaran(saldo):
    while True:
         try:     
          print(f'saldo masuk {saldo}')
          uang_keluar= int(input('Masukan uang pengeluaran: '))
          if uang_keluar <= 0:
            print('Uang harus lebih dari 0')
            continue
          elif uang_keluar > saldo:
             print('Saldo anda tidak mencukupi')
             continue
          saldo = saldo - uang_keluar
          print(f'Saldo anda sebesar Rp.{saldo}')
         except ValueError:
            print('Input harus angka!!')
            continue
         break
    return uang_keluar

def riwayat(saldo):
   print('Saldo anda tersedia Rp.{saldo:.2f} ')
