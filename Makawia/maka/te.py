import serial,time

phone = serial.Serial('COM15', 115200, timeout=5)

rsp = []
phone.write(('AT+CUSD=1,"*150*01#",\r').encode())
time.sleep(1)
m = phone.readlines()
for i in m:
    rsp.append(i.decode())
for j in range(3, len(rsp)):
    print(rsp[j])

print("Enter a number: ")
num = input()
if int(num) == 1:
    phone.write(('AT+CUSD=2,15\r').encode())
    time.sleep(1)
    m = phone.readlines()
    for i in m:
        rsp.append(i.decode())
    for j in range(3, len(rsp)):
        print(rsp[j])
else:
    print("Enter a number: ")
    num = input()
    if num == 1:
        phone.write(('AT+CUSD=2,\r').encode())
