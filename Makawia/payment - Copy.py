import sys, serial, time, mysql.connector, serial.tools.list_ports
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget,
                             QVBoxLayout, QListWidget, QListWidgetItem,QLineEdit)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer
from PyQt5.QtGui import QPixmap, QFont,QIcon
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

    def gotomessages(self):
        widget.setCurrentIndex(7)

    def gotocontacts(self):
        widget.setCurrentIndex(9)


class Loginpage(QDialog):
    def __init__(self):
        super(Loginpage, self).__init__()
        loadUi("maka/loginpage.ui", self)
        self.wrong1.hide()
        self.wrong2.hide()
        self.empty.hide()
        self.login.clicked.connect(self.gotohomepage)
        self.create.clicked.connect(self.gotoregisterpage)
        self.stata = False

    def gotoregisterpage(self):
        widget.setCurrentIndex(1)


    def gotohomepage(self):
        lst = []
        pn = self.pnm.text()
        ps = self.ps.text()
        db = mysql.connector.connect(host="localhost", user="root", password="root", database='USERS')
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
                count1 = 0
                count2 = 0
                count3 = 0
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

                        messagepage = Messagepage()
                        messagepage.nmm.setText(name)
                        messagepage.pnmm.setText(pn)
                        widget.addWidget(messagepage)

                        newmessagepage = NewMessagepage()
                        newmessagepage.nmm.setText(name)
                        newmessagepage.pnmm.setText(pn)
                        widget.addWidget(newmessagepage)

                        contactpage = Contactpage()
                        contactpage.nmm.setText(name)
                        contactpage.pnmm.setText(pn)
                        widget.addWidget(contactpage)
                        

                        self.thds = []
                        self.thds.append(Thread(target=homepage.Dsts))
                        self.thds.append(Thread(target=transactionpage.Dsts))
                        self.thds.append(Thread(target=sendpage.Dsts))
                        self.thds.append(Thread(target=withdrawpage.Dsts))
                        self.thds.append(Thread(target=paypage.Dsts))
                        self.thds.append(Thread(target=messagepage.Dsts))
                        self.thds.append(Thread(target=newmessagepage.Dsts))
                        self.thds.append(Thread(target=contactpage.Dsts))



                        for thd in self.thds:
                            thd.start()
                        self.stata = True

                        widget.setCurrentIndex(2)
                        self.ps.setText('')


                    elif pn != tm.split('.')[0] and ps == tm.split('.')[1]:
                        self.wrong1.show()
                        QTimer.singleShot(2000, self.wrong1.hide)
                        count1 += 1

                    elif pn == tm.split('.')[0] and ps != tm.split('.')[1]:
                        count2 += 1

                    elif pn != tm.split('.')[0] and ps != tm.split('.')[1]:
                        count3 += 1

                if count1 > 0:
                    self.wrong1.show()
                    QTimer.singleShot(2000, self.wrong1.hide)
                elif count2 > 0:
                    self.wrong2.show()
                    QTimer.singleShot(2000, self.wrong2.hide)
                elif count3 > 0:
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
        stote = False

        if ps == cps and fnm != '' and mnm != '':
            stote = True

        elif ps == cps and fnm != '' and snm != '':
            stote = True

        else:
            self.db1.show()
            self.db2.show()
            QTimer.singleShot(2000, self.db1.hide)
            QTimer.singleShot(2000, self.db2.hide)

        if stote == True:
            db = mysql.connector.connect(host="localhost", user="root", password="root", database='USERS')
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
        self.messages.clicked.connect(unb.gotomessages)
        self.contacts.clicked.connect(unb.gotocontacts)


    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)

            time.sleep(2)
            if state == False:
                break


class Messagepage(QDialog):
    def __init__(self):
        super(Messagepage, self).__init__()
        loadUi("maka/msg.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)
        self.nw.clicked.connect(self.gotonewmessage)
        self.rd.clicked.connect(self.retrieve)
        self.contacts.clicked.connect(unb.gotocontacts)
        




    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)

            time.sleep(2)
            if state == False:
                break
            
    def gotonewmessage(self):
        widget.setCurrentIndex(8)

        

    def retrieve(self):
        wdgt = QWidget()
        vbox = QVBoxLayout()
        wdgt.setLayout(vbox)
        self.scroll.setWidget(wdgt)
        ls = QListWidget()
        rsp = []
        rspp = []
        phone = serial.Serial(thread.pt, 115200, timeout=5)
        phone.write(('AT+CMGF=1\r').encode())
        time.sleep(1)
        phone.write(('AT+CMGL="ALL"\r').encode())
        time.sleep(1)
        m = phone.readlines()
        for i in range(5,len(m)):
            rsp.append(m[i].decode())
            
        m = 1
        n = 0
        for i in rsp:
            stit = True
            if i.split(':')[0] == '+CMGL':
                try:
                    if stit == True:
                        a = rsp[n].split('""')[-1].split('+')[0].split('"')[1].split(',')[0]
                        b = rsp[n].split('""')[-1].split('+')[0].split('"')[1].split(',')[1]
                        c = rsp[n].split('"REC READ","')[1].split('",')[0]
                        QListWidgetItem(str(m)+'. '+c+'   '+a+ '   '+b+'\n',ls)
                        ls.setFont(QFont('Arial', 13))
                        ls.setStyleSheet("QLabel""{""border : 1px solid black;""background : white;""}")
                        vbox.addWidget(ls)
                        stit = False
                    m+=1
                except:
                    try:
                        p = rsp[n].split('UNSENT","')[1].split('"')[0]
                    except:
                        p = rsp[n]
                        QListWidgetItem(p,ls)
                        ls.setFont(QFont('Arial', 13))
                        ls.setStyleSheet("QLabel""{""border : 1px solid black;""background : white;""}")
                        vbox.addWidget(ls)
            else:
                QListWidgetItem(rsp[n],ls)
                ls.setFont(QFont('Arial', 13))
                ls.setStyleSheet("QLabel""{""border : 1px solid black;""background : white;""}")
                vbox.addWidget(ls)            
            n+=1
            

class NewMessagepage(QDialog):
    def __init__(self):
        super(NewMessagepage, self).__init__()
        loadUi("maka/messagepage.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.messages.clicked.connect(unb.gotomessages)
        self.transaction.clicked.connect(unb.gototransaction)
        self.contacts.clicked.connect(unb.gotocontacts)
        self.send.clicked.connect(self.sendmessage)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)
            time.sleep(2)
            if state == False:
                break

    def sendmessage(self):
        try:
            phone = serial.Serial("COM6", 115200, timeout=5)
            rsp = []
            phone.write(('AT+CMGF=1\r').encode())
            time.sleep(1)
            phone.write(('AT+CMGS="'+self.num.text()+'"\r').encode())
            time.sleep(1)
            phone.write((self.txt.toPlainText()).encode())
            time.sleep(1)
            phone.write(bytes([26]))
            time.sleep(1)
        finally:
            phone.close()

    
class Contactpage(QDialog):
    def __init__(self):
        super(Contactpage, self).__init__()
        loadUi("maka/contacts.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.messages.clicked.connect(unb.gotomessages)
        self.transaction.clicked.connect(unb.gototransaction)
        self.rd.clicked.connect(self.retrieve)


    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)
            time.sleep(2)
            if state == False:
                break

    def retrieve(self):
        wdgt = QWidget()
        vbox = QVBoxLayout()
        wdgt.setLayout(vbox)
        self.scroll.setWidget(wdgt)
        ls = QListWidget()
        phone = serial.Serial("COM6", 115200, timeout=5)
        rsp = []
        rspp = []
        phone.write(('AT+CPBR=1,6\r').encode())
        time.sleep(1)
        m = phone.readlines()
        for i in m:
            rsp.append(i.decode())
        n = 1
        for j in range(1,len(rsp)):
            try:
                a = rsp[j].split('",')[1].split(',"')[1].split('"')[0]
                b = rsp[j].split('",')[0].split(',"')[1]
                QListWidgetItem(str(n)+'.'+a+'\n'+'   '+b+'\n\n',ls)
                ls.setFont(QFont('Arial', 13))
                ls.setStyleSheet("QLabel""{""border : 1px solid black;""background : white;""}")
                vbox.addWidget(ls)
                n += 1
            except:
                pass
        


class Transactionpage(QDialog):
    def __init__(self):
        super(Transactionpage, self).__init__()
        loadUi("maka/transactionpage.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.send.clicked.connect(self.gotosendpage)
        self.withdraw.clicked.connect(self.gotowithdrawpage)
        self.pay.clicked.connect(self.gotopaypage)
        self.messages.clicked.connect(unb.gotomessages)
        self.contacts.clicked.connect(unb.gotocontacts)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)

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
        self.yes.hide()
        self.no.hide()
        self.cmnt1.hide()
        self.cmnt2.hide()
        self.cmnt3.hide()
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)
        self.messages.clicked.connect(unb.gotomessages)
        self.contacts.clicked.connect(unb.gotocontacts)
        self.send.clicked.connect(self.thrding)
        self.yes.clicked.connect(self.yeser)
        self.no.clicked.connect(self.noer)
        self.pb.setStyleSheet("QProgressBar::chunk ""{"
                              "background-color: rgb(189, 0, 0);""}")

        self.ps = ''
        self.stt = True
        self.killussd = False
        self.opt = ''
        self.countt = ''
        self.sta = False

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)

            time.sleep(2)
            if state == False:
                break

    def thrding(self):
        try:
            print(self.a.isAlive())
            if self.a.isAlive() == True:
                self.a.join()
                time.sleep(2)
                self.sto = False
                self.send.hide()
                self.phone = serial.Serial(thread.pt, 115200, timeout=5)
                self.a = Thread(target=self.runner)
                self.a.start()

            else:
                self.sto = False
                self.send.hide()
                self.phone = serial.Serial(thread.pt, 115200, timeout=5)
                self.a = Thread(target=self.runner)
                self.a.start()

        except:
            self.sto = False
            self.send.hide()
            self.phone = serial.Serial(thread.pt, 115200, timeout=5)
            self.a = Thread(target=self.runner)
            self.a.start()

    def runner(self):
        self.rc.setText('')
        self.cmnt1.hide()
        self.cmnt2.hide()
        self.mn1 = []
        nmbr = []
        pnm = self.pnm.text()
        amnt = self.amnt.text()
        self.ps = self.pn.text()
        if pnm != '' and self.ps != '' and amnt != '':
            for i in range(len(pnm)):
                nmbr.append(pnm[i])
            while True:
                if thread.smc == 'TIGO':
                    if nmbr[0] + nmbr[1] + nmbr[2] == '071' or nmbr[0] + nmbr[1] + \
                            nmbr[2] == '067' or nmbr[0] + nmbr[1] + nmbr[2] == '065':
                        if self.mn1 == []:
                            self.opt = '*150*01#'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(100 / 6))
                        elif self.mn1 == ['*150*01#']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(200 / 6))
                        elif self.mn1 == ['*150*01#', '1']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(300 / 6))
                        elif self.mn1 == ['*150*01#', '1', '1']:
                            self.opt = pnm
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(400 / 6))
                        elif self.mn1 == ['*150*01#', '1', '1', pnm]:
                            self.opt = amnt
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(500 / 6))
                            self.yes.show()
                            self.no.show()
                            self.rc.setText((self.nm.split('-')[1]).split('.')[0])

                    else:
                        if nmbr[0] + nmbr[1] + nmbr[2] == '075' or nmbr[0] + nmbr[1] \
                                + nmbr[2] == '076' or nmbr[0] + nmbr[1] + nmbr[2] == '074':
                            chc3 = '3'
                        elif nmbr[0] + nmbr[1] + nmbr[2] == '068' or nmbr[0] + nmbr[1] + nmbr[2] == '078':
                            chc3 = '1'
                        elif nmbr[0] + nmbr[1] + nmbr[2] == '062':
                            chc3 = '5'

                        if self.mn1 == []:
                            self.opt = '*150*01#'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(100 / 7))
                        elif self.mn1 == ['*150*01#']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(200 / 7))
                        elif self.mn1 == ['*150*01#', '1']:
                            self.opt = '3'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(300 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3']:
                            self.opt = chc3
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(400 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3', chc3]:
                            self.opt = pnm
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(500 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3', chc3, pnm]:
                            self.opt = amnt
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(600 / 7))
                            self.yes.show()
                            self.no.show()
                            nm = (self.nm.split('-')[0]).split(' ')
                            try:
                                if nm[-4].isupper() == True:
                                    self.rc.setText(nm[-4] + ' ' + nm[-3] + ' ' + nm[-2])
                                else:
                                    self.rc.setText(nm[-3] + ' ' + nm[-2])
                            except:
                                try:
                                    self.rc.setText(nm[-3] + ' ' + nm[-2])
                                except:
                                    pass
                            
                            

                        elif self.sta == True:
                            self.opt = self.ps
                            self.responder()
                            self.fund_value()
                            self.send.show()
                            self.pb.setValue(100)
                            self.sto = True
                            self.sta = False

                    if self.sto == True:
                        break

                elif thread.smc == 'VODACOM':
                    if nmbr[0] + nmbr[1] + nmbr[2] == '075' or nmbr[0] + nmbr[1] \
                            + nmbr[2] == '076' or nmbr[0] + nmbr[1] + nmbr[2] == '074':
                        if self.mn1 == []:
                            self.opt = '*150*01#'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(100 / 6))
                        elif self.mn1 == ['*150*01#']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(200 / 6))
                        elif self.mn1 == ['*150*01#', '1']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(300 / 6))
                        elif self.mn1 == ['*150*01#', '1', '1']:
                            self.opt = pnm
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(400 / 6))
                        elif self.mn1 == ['*150*01#', '1', '1', pnm]:
                            self.opt = amnt
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(500 / 6))
                            self.yes.show()
                            self.no.show()
                            self.rc.setText((self.nm.split('-')[1]).split('.')[0])

                    else:
                        if nmbr[0] + nmbr[1] + nmbr[2] == '071' or nmbr[0] + nmbr[1] + \
                                nmbr[2] == '067' or nmbr[0] + nmbr[1] + nmbr[2] == '065':
                            chc3 = '3'
                        elif nmbr[0] + nmbr[1] + nmbr[2] == '068' or nmbr[0] + nmbr[1] + nmbr[2] == '078':
                            chc3 = '1'
                        elif nmbr[0] + nmbr[1] + nmbr[2] == '062':
                            chc3 = '5'

                        if self.mn1 == []:
                            self.opt = '*150*01#'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(100 / 7))
                        elif self.mn1 == ['*150*01#']:
                            self.opt = '1'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(200 / 7))
                        elif self.mn1 == ['*150*01#', '1']:
                            self.opt = '3'
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(300 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3']:
                            self.opt = chc3
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(400 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3', chc3]:
                            self.opt = pnm
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(500 / 7))
                        elif self.mn1 == ['*150*01#', '1', '3', chc3, pnm]:
                            self.opt = amnt
                            self.mn1.append(self.opt)
                            self.responder()
                            self.pb.setValue(int(600 / 7))
                            self.yes.show()
                            self.no.show()
                            nm = (self.nm.split('-')[0]).split(' ')
                            self.rc.setText(nm[-3] + ' ' + nm[-2])

    def responder(self):
        rsp = []
        self.phone.write(('AT+CUSD=1' + ',"' + self.opt + '",' + '15\r').encode())
        time.sleep(1)
        m = self.phone.readlines()
        for i in m:
            rsp.append(i.decode())
        for j in range(3, len(rsp)):
            self.nm = []
            print(rsp[j])
            self.nm = rsp[j]
        if self.sta == True:
            self.phone.write(('AT+CUSD=2,15\r').encode())
            time.sleep(1)
            m = self.phone.readlines()
            for i in m:
                print(i.decode())
            self.phone.close()
            self.pb.setValue(100)


    def yeser(self):
        self.sta = True
        self.yes.hide()
        self.no.hide()

    def noer(self):
        self.yes.hide()
        self.no.hide()
        self.sto = True
        self.phone.write(('AT+CUSD=2,15\r').encode())
        time.sleep(1)
        m = self.phone.readlines()
        for i in m:
            print(i.decode())
        self.cmnt3.show()
        self.pb.setValue(100)
        self.send.show()
        self.phone.close()

    def fund_value(self):
        if ((self.nm).split(' ')[8]) == 'salio':
            self.cmnt2.show()
        else:
            self.cmnt1.show()


class Withdrawpage(QDialog):
    def __init__(self):
        super(Withdrawpage, self).__init__()
        loadUi("maka/withdraw.ui", self)
        self.hm.clicked.connect(unb.gotohome)
        self.lgo.clicked.connect(unb.gotologin)
        self.transaction.clicked.connect(unb.gototransaction)
        self.messages.clicked.connect(unb.gotomessages)
        self.contacts.clicked.connect(unb.gotocontacts)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)
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
        self.messages.clicked.connect(unb.gotomessages)
        self.contacts.clicked.connect(unb.gotocontacts)

    def Dsts(self):
        while True:
            self.st.setText(thread.stt)
            self.sm.setText(thread.sim)
            self.smcd.setText(thread.smc)
            time.sleep(2)
            if state == False:
                break


class Detectdevice():
    def __init__(self):
        super(Detectdevice, self).__init__()
        self.sim = ''
        self.smc = ''
        self.pt = ''
        self.tmm = 2
        self.state1 = True
        self.rsppp = []


    def runn(self):
        while True:
            ports = serial.tools.list_ports.comports()
            count = 0
            for port, desc, hwid in sorted(ports):
                if desc == 'USB-SERIAL CH340 (' + port + ')':
                    self.pt = port
                    count += 1
            if count > 0:
                self.stt = 'Connected'
                if self.state1 == True:
                    self.chksmcd()
                    self.state1 = False

            else:
                self.stt = 'Not Connected'
                self.sim = ''
                self.smc = ''
                self.tmm = 7
                self.state1 = True
            if state == False:
                break

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
                ids = ['64002', '64004']
                idsn = ['TIGO','VODACOM']
                try:
                    for id in range(len(ids)):
                        phone.write(('AT+COPS=1,2,"' + ids[id] + '"\r').encode())
                        time.sleep(1)
                        try:
                            mm = phone.readlines()
                            nn = (mm[1].decode()).split()
                            if nn[0].split()[0] == 'OK':
                                self.smc = idsn[id]
                                phone.close()
                        except:
                            time.sleep(0)
                except:
                    time.sleep(0)
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
state = True
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
    if loginpage.stata == True:
        thread.kill()
    print("Exiting")

