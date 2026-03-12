from function import Pemasukan,Pengeluaran,Riwayat
print('=======Tabungan Kita=======\n')
# try:
#   with open("saldo.txt""r")as file:
#      saldo = (int(file.read))
# except:
riwayat = []
saldo = 0
while True:
    print('Pilih Program!')
    print('1.Input Pemasukan')
    print('2.Input Pengeluaran')
    print('3.Lihat Total')
    print('4.Reset Total')
    print('0.Keluar\n')
    user = input('Silahkan pilih program yang ada: ')

    if user == '1':
     saldo = Pemasukan(saldo,riwayat)
     
    #  with open("saldo.txt","a")as file:
    #    file.write(str(saldo))

    elif user == '2':
     saldo = Pengeluaran(saldo,riwayat)

    #  with open("saldo.txt","r")as file:
    #    file.write(str(saldo))
       
    elif user == '3':
      Riwayat(riwayat)

    elif user == '4':
       reset = input('Apakah ingin mereset saldo anda?[y/n]: ')
       if reset == 'y':
         saldo = 0
         print(f'Saldo berhasil direset Rp.{saldo}')
       elif reset == 'n':
         print()
         continue

    elif user == '0':
     print('Program selesai🙏!')
     break

    else:
     print('Input tidak valid!')
    continue
   
       



