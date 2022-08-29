import sys,serial,time, mysql.connector,serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QDialog, QApplication)
from PyQt5.QtCore import QTimer
from threading import Thread



class UniversalButtons(QDialog):
    def __init__(self):
        super(UniversalButtons, self).__init__()
        loadUi("maka/loginpage.ui", self)

    def gotohome(self):
        widget.setCurrentIndex(2)

    def gototransaction(self):
        widget.setCurrentIndex(3)

    def gotologin(self):
        widget.setCurrentIndex(0)


class Loginpage(QDialog):
    def __init__(self):
        super(Loginpage, self).__init__()
        loadUi("maka/loginpage.ui", self)
        self.wrong1.hide()
        self.wrong2.hide()
        self.empty.hide()
        self.login.clicked.connect(self.gotohomepage)
        self.create.clicked.connect(self.gotoregisterpage)

    def gotoregisterpage(self):
        widget.setCurrentIndex(1)

    def gotohomepage(self):
        lst = []
        pn = self.pnm.text()
        ps = self.ps.text()
        db = mysql.connector.connect(host="localhost", user="jonpol", password="root", database='USERS')
        cursor = db.cursor()
        cursor.execute("select exists(select 1 from users) as OUTPUT")
        for itm in cursor:
            if itm[0] == 0:
                self.empty.show()
                QTimer.singleShot(2000, self.empty.hide)
            else:
                cursor.reset()
                cursor.execute("select PHONE_NO,PS,USER_NAME from users")
                for itm in cursor:
                    lst.append(itm[0] + '.' + itm[1] + '.' + itm[2])
                for tm in lst:
                    if pn == tm.split('.')[0] and ps == tm.split('.')[1]:
                        name = tm.split('.')[2]

                        homepage = Homepage()
                        homepage.nmm.setText(name)
                        homepage.pnmm.setText(pn)
                        widget.addWidget(homepage)

                        transactionpage = Transactionpage()
                        transactionpage.nmm.setText(name)
                        transactionpage.pnmm.setText(pn)
                        widget.addWidget(transactionpage)

                        sendpage = Sendpage()
                        sendpage.nmm.setText(name)
                        sendpage.pnmm.setText(pn)
                        widget.addWidget(sendpage)

                        withdrawpage = Withdrawpage()
                        withdrawpage.nmm.setText(name)
                        withdrawpage.pnmm.setText(pn)
                        widget.addWidget(withdrawpage)

                        paypage = Paypage()
                        paypage.nmm.setText(name)
                        paypage.pnmm.setText(pn)
                        widget.addWidget(paypage)

                        self.thds = []
                        self.thds.append(Thread(target=homepage.Dsts))
                        self.thds.append(Thread(target=transactionpage.Dsts))
                        self.thds.append(Thread(target=sendpage.Dsts))
                        self.thds.append(Thread(target=withdrawpage.Dsts))
                        self.thds.append(Thread(target=paypage.Dsts))

                        for thd in self.thds:
                            thd.start()

                        widget.setCurrentIndex(2)
                        self.ps.setText('')

                    elif pn != tm.split('.')[0] and ps == tm.split('.')[1]:
                        self.wrong1.show()
                        QTimer.singleShot(2000, self.wrong1.hide)

                    elif pn == tm.split('.')[0] and ps != tm.split('.')[1]:
                        self.wrong2.show()
                        QTimer.singleShot(2000, self.wrong2.hide)

                    else:
                        self.wrong1.show()
                        self.wrong2.show()
                        QTimer.singleShot(2000, self.wrong1.hide)
                        QTimer.singleShot(2000, self.wrong2.hide)


class Registerpage(QDialog):
    def __init__(self):
        super(Registerpage, self).__init__()
        loadUi("maka/registerpage.ui", self)
        self.db1.hide()
        self.db2.hide()
        self.dn.hide()
        self.regist.clicked.connect(self.Registeruser)
        self.goback.clicked.connect(self.gotologinpage)

    def Registeruser(self):
        fnm = self.fnm.text()
        mnm = self.mnm.text()
        snm = self.snm.text()
        nm = self.nm.text()
        ps = self.ps.text()
        cps = self.cps.text()
        state = False

        if ps == cps and fnm != '' and  mnm != '':
            state = True

        elif ps == cps and fnm != '' and snm != '':
            state = True

        else:
            self.db1.show()
            self.db2.show()
            QTimer.singleShot(2000, self.db1.hide)
            QTimer.singleShot(2000, self.db2.hide)

        if state == True:
            db = mysql.connector.connect(host="localhost", user="jonpol", password="root", database='USERS')
            cursor = db.cursor()
            sql = "insert into users (USER_NAME,PHONE_NO,PS,CPS) values(%s,%s,%s,%s)"
            val = (fnm + " " + mnm + " " + snm, nm, ps, cps)
            cursor.execute(sql, val)
            self.dn.show()
            QTimer.singleShot(2000, self.dn.hide)
            cursor.close()
            db.commit()



    def gotologinpage(self):
        widget.setCurrentIndex(0)


class Homepage(QDialog):
    def __init__(self):
        super(Homepage, self).__init__()
        loadUi("maka/homepage.ui", self)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            time.sleep(2)
            if state == False:
                break


class Transactionpage(QDialog):
    def __init__(self):
        super(Transactionpage, self).__init__()
        loadUi("maka/transactionpage.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.send.clicked.connect(self.gotosendpage)
        self.withdraw.clicked.connect(self.gotowithdrawpage)
        self.pay.clicked.connect(self.gotopaypage)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            time.sleep(2)
            if state == False:
                break

    def gotosendpage(self):
        widget.setCurrentIndex(4)

    def gotowithdrawpage(self):
        widget.setCurrentIndex(5)

    def gotopaypage(self):
        widget.setCurrentIndex(6)


class Sendpage(QDialog):
    def __init__(self):
        super(Sendpage, self).__init__()
        loadUi("maka/send.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)
        self.send.clicked.connect(self.runner)
        

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            time.sleep(2)
            if state == False:
                break

    def responder(self):
        phone = serial.Serial("COM15", 115200, timeout=5)
        rsp = []
        phone.write(('AT+CUSD=1' + ',"' + self.opt + '",' + '\r').encode())
        time.sleep(1)
        m = phone.readlines()
        for i in m:
            rsp.append(i.decode())
        for j in range(3, len(rsp)):
            self.nm = []
            print(rsp[j])
            self.nm.append(rsp[j])


    def runner(self):
        nmbr = []
        pnm = self.pnm.text()
        amnt = self.amnt.text()
        ps = self.pn.text()
        for i in range(len(pnm)):
            nmbr.append(pnm[i])
        self.opt = '*150*01#'
        self.responder()
        if nmbr[0] + nmbr[1] + nmbr[2] == '065' or nmbr[0] + nmbr[1] + nmbr[2] == '071':
            prcs = ['1', '1']
            for itm in range(len(prcs)):
                self.opt = prcs[itm]
                self.responder()
            self.opt = pnm
            self.responder()
            self.opt = amnt
            self.responder()
            self.opt = ps
            self.responder()

        if nmbr[0] + nmbr[1] + nmbr[2] == '074' or nmbr[0] + nmbr[1] + nmbr[2] == '076' or nmbr[0] + nmbr[1] + nmbr[2] == '075':           
            self.opt = '1'
            self.responder()
            self.opt = '3'
            self.responder()
            self.opt = '3'
            self.responder()
            self.opt = pnm
            self.responder()
            self.opt = amnt
            self.responder()
            self.opt = ps
            self.responder()
            

class Withdrawpage(QDialog):
    def __init__(self):
        super(Withdrawpage, self).__init__()
        loadUi("maka/withdraw.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            time.sleep(2)
            if state == False:
                break


class Paypage(Homepage):
    def __init__(self):
        super(Paypage, self).__init__()
        loadUi("maka/pay.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            time.sleep(2)
            if state == False:
                break


class Detectdevice():
    def __init__(self):
        super(Detectdevice, self).__init__()
        self.sim = ''
        self.tmm = 0
        self.state1 = True


    def runn(self):
        while True:
            ports = serial.tools.list_ports.comports()
            count = 0
            for port, desc, hwid in sorted(ports):
                if desc == 'USB-SERIAL CH340 (' + port + ')':
                    self.pt = port
                    count+=1
            if count > 0:
                self.stt = 'Connected'
                if self.state1 == True:
                    self.chksmcd()
                    self.state1 = False

            else:
                self.stt = 'Not Connected'
                self.sim = ''
                self.tmm = 8
                self.state1 = True
            if state == False:
                break
            time.sleep(2)

    def chksmcd(self):
        try:
            time.sleep(self.tmm)
            phone = serial.Serial(self.pt, 115200, timeout=5)
            phone.write(('AT+CPIN?\r').encode())
            time.sleep(1)
            m = phone.readlines()
            n = (m[1].decode()).split()
            if n[1] == 'READY':
                self.sim = 'SIMCARD'
            else:
                self.sim = 'NO SIMCARD'
        except:
            self.sim = 'NO SIMCARD'

    def kill(self):
        time.sleep(1)
        for thds in loginpage.thds:
            thds.join()


# main
app = QApplication(sys.argv)
global state
state=True
thread = Detectdevice()
thrd1 = Thread(target=thread.runn)
thrd1.start()
unb = UniversalButtons()
widget = QtWidgets.QStackedWidget()
loginpage = Loginpage()
widget.addWidget(loginpage)
registerpage = Registerpage()
widget.addWidget(registerpage)
widget.setFixedWidth(852)
widget.setFixedHeight(581)
widget.setCurrentIndex(0)
widget.show()



try:
    sys.exit(app.exec_())
except:
    state = False
    thrd1.join()
    thread.kill()
    print("Exiting")

