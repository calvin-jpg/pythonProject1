#get contacts
import sys, serial, time, mysql.connector, serial.tools.list_ports
from threading import Thread
def responder():
    phone = serial.Serial("COM6", 115200, timeout=5)
    rsp = []
    rspp = []
    '''phone.write(('AT+CPBS=\"SM\""\r').encode())
    time.sleep(1)'''
    phone.write(('AT+CPBR=1,6\r').encode())
    time.sleep(1)
   

    m = phone.readlines()
    for i in m:
        rsp.append(i.decode())
    for j in range(1,len(rsp)):
        try:
            print(rsp[j].split('",')[1].split(',"')[1].split('"')[0])
            print(rsp[j].split('",')[0].split(',"')[1])
        except:
            pass
        
responder()

