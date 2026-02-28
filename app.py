from function import Pemasukan,Pengeluaran
print('=======TabunganKita=======\n')
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
     saldo = Pemasukan(saldo)

    elif user == '2':
     saldo = Pengeluaran(saldo)

    elif user == '0':
     print('Program selesai🙏!')
     break

    else:
     print('Input tidak valid!')
    continue
   
       



