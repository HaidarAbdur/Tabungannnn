# def Pemasukan(saldo,riwayat):
#   while True:
#        saldo = 0
#        try:
#         uang = int(input('Masukan uang pemasukan: '))
#         saldo += uang
#         riwayat.append(f"Pemasukan Rp.{uang}")
#         if uang <= 0:
#             print('Uang harus lebih dari 0')
#             continue
#         elif uang >= 0:
#             print(f'Saldo berhasil ditambahkan sebesar Rp.{uang}')
#        except ValueError:
#            print('Input harus berupa angka')
#            continue
#        break
#   return saldo

# def Pengeluaran(saldo,riwayat):
#     while True:
#          try:     
#           print(f'Saldo anda sekarang Rp.{saldo}')
#           uang_keluar= int(input('Masukan uang pengeluaran: '))
#           note = input('Catatan pengeluaran: ')
#          #  if note:
#          #     print()
#           if uang_keluar <= 0:
#             print('Uang harus lebih dari 0')
#             continue
#           elif uang_keluar >= saldo: 
#              print('Maaf,saldo tidak cukup')
#           else:
#            saldo -= uang_keluar
#            print(f'Saldo anda sekarang sebesar Rp.{saldo}')
#          except ValueError:
#             print('Input harus angka!!')
#             continue
#          riwayat.append ((uang_keluar, note))
#          break
#     return saldo
 
# def Riwayat(riwayat):
#    if len(riwayat) == 0:
#       print('Belum ada riwayat transaksi')
#       return
   
#    print('======RIWAYAT TRANSAKSI======')

#    nomor = 1
#    for transaksi in riwayat:
#       print(f'{nomor}. {transaksi}')
#       nomor += 1


  

   