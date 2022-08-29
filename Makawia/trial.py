import sys, serial, time, mysql.connector, serial.tools.list_ports
from threading import Thread
def responder():

    phone = serial.Serial("COM7", 115200, timeout=5)
    rsp = []
    rspp = []
    phone.write(('AT+CPBS=\"SM\""\r').encode())
    time.sleep(1)
    phone.write(('AT+CPBR=1,6\r').encode())
    time.sleep(1)
    m = phone.readlines()
    for i in m:
        rsp.append(i.decode())
        m = 1
        n = 0
        for i in rsp:
            stt = True
            if i.split(':,')[0] == '+CPBR':
                for j in range(5):
                    if stt == True:
                        a = rsp[n].split('""')[-1].split(',"')[0].split('",')[1].split(',"')[0]
                #b = rsp[n].split(',,')[-1].split('+')[0].split('"')[1].split(',')[1]
                #c = rsp[n].split('"REC READ","')[1].split('",')[0]
                        print(str(m)+'.    '+a+ '   \n')
                        stt = False
                        print(rsp[n+j+1])
                        n+=1
                        m+=1
   
    

    



responder()  
'''for j in range(1, len(rsp)):
    print(rsp[j])'''
