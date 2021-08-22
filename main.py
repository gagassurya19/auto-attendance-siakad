import scriptabsen
import values
from account.getaccount import getaccount

import pytz
from time import time, sleep
from datetime import datetime
import concurrent.futures


print("Jumlah User: " + str(len(getaccount())))
print(getaccount())
print("Ready")


while True:
    sleep(5 - time() % 5)

    WIB = pytz.timezone('Asia/Jakarta')
    time_now = datetime.now(WIB)

    if (time_now.strftime('%H') == '05' and 
            time_now.strftime('%M') == '58' and
            time_now.strftime('%a') != 'Sat' and
            time_now.strftime('%a') != 'Sun'):

        def run(account):
            temp = scriptabsen.runscript(account, values.sitelogger(), values.browser())
            times = datetime.now(WIB)
            if(temp == True):
                print("Absen berhasil pada " + times.strftime('%c'))
            elif(temp == False):
                print("Absen gagal, SERVER SEKOLAH KENTANK, mencoba lagi " +
                        times.strftime('%c'))
                ass = scriptabsen.override(account, values.sitelogger(), values.browser())
                if ass == True:
                    timee = datetime.now(WIB)
                    print("Absen berhasil pada " + timee.strftime('%c'))
                else:
                    print("Gagal akses website")
            else:
                print("Server-mu Down " + times.strftime('%c'))
        
        if __name__ == '__main__':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # data account
                accounts = getaccount()
                results = executor.map(run, accounts)

        print(f'finished')
