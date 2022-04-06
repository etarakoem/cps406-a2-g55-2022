import textDatabase as td
from datetime import date
import os


class Email:
    def __init__(self):
        self.receiver = ''
        self.sender = ''
        self.content = ''
        self.header = ''
        self.date = date.today()

    def anEmail(self,sender: str,receiver: str,header: str,content: str):
        self.sender = sender
        self.receiver = receiver
        self.date = date.today()
        self.header = header
        self.content = content

    def getSender(self):
        return self.sender
    def getReceiver(self):
        return self.receiver
    def getDate(self):
        return self.date
    def getHeader(self):
        return self.header
    def stripContent(self):
        content = self.content
        return content.replace('(n)','\n')
    def getContent(self):
        return self.content

    def viewMailOptions(self,userbox):
        print(f"{'Email ID':10} | {'Email title':25} | {'From':25}")
        for i in range(len(userbox)):
            print(f"{i:10} | {userbox[i][3]:25} | {userbox[i][1]:25}")
        command = input('Checking email ID: ')
        return self.viewFullMail(userbox[int(command)])

    def viewFullMail(self,mail):
        print("=============================")
        self.setDate(mail[0])
        self.anEmail(mail[1],mail[2],mail[3],mail[4])
        self.viewEmail()
        print("=======End of Email==========")
        enter = input("Press Enter to continue.....")
        return

    def viewEmail(self):
        print("{} \nFrom: {} \nTo: {} \nTitle: {} \n\n{}".format(self.getDate(),self.getSender(),self.getReceiver(),self.getHeader(),self.stripContent()))

    def toDB(self):
        return str(self.getDate()) + ":" + self.getSender()+ ":" +self.getReceiver()+ ":" +self.getHeader()+ ":" +self.getContent()+"\n"

    def setSender(self,sender):
        self.sender = sender

    def setDate(self,date):
        self.date = date

    def setReceiver(self):
        receiver = input('Receiver: ')
        self.receiver = receiver

    def setHeader(self):
        title = input('Email Title: ')
        self.header = title

    def finishMSG(self,msg):
        if msg == 'd':
            return True
        return False

    def setContent(self):
        print('Typing your email, once done, type "d"')
        msg = input('Message: \n')
        while (not self.finishMSG(msg)):
            self.content += msg + '(n)'
            msg = input('> ')

    def compose(self,sender):
        self.setSender(sender)
        self.setHeader()
        self.setReceiver()
        self.setContent()
        self.viewEmail()
        command = input('Satisfy with your email? [y/N] ')
        if command == 'y' or command == 'Y':
            self.sendEmail('email_db')
            print('Email sent to ', self.getReceiver())
            return
        else:
            command = input('Recompose? [y/N] ')
            if command == 'y' or command == 'Y':
                return self.compose()
            else:
                return

    def sendEmail(self,box: str):
        db = td.textDB()
        db.openDB(box)
        db.insert(self.toDB())


    def findMailsOf(self,box: str,receiver: str):
        db = td.textDB()
        mailBox = db.retrieve(box)
        userBox = [mail for mail in mailBox if mail[2] == receiver]
        return userBox


def createEmailDB():
    db = td.textDB()
    db.createDB('email_db')

def sendEmail(email: Email,box:str):
    db = td.textDB()
    db.openDB(box)
    db.insert(email.toDB())

def findMailsOf(receiver: str,box: str):
    db = td.textDB()
    mailBox = db.retrieve(box)
    userBox = [mail for mail in mailBox if mail[1] == receiver]
    return userBox

def main():
    email = Email()
    email.anEmail('Admin','Example','Test Email','Just a quick Email here (n)How are you?')
    print(email.viewEmail())
    #sendEmail(email,'email_db')
    adminMails = findMailsOf('Admin','email_db')
    for i in adminMails:
        print(i)
    email.anEmail('Staff','Example','Test Staff','Content (n) New Line (n) New Line')
    for i in range(2):
        sendEmail(email,'email_db')
    staffMails = findMailsOf('Staff','email_db')
    for i in staffMails:
        print(i)
def test1():
    email = Email()
    email.setSender('Etarakoem')
    email.compose()
    email.viewEmail()
    command = input('Satisfy with your email? [y/N] ')
    if command == 'y' or command == 'Y':
        sendEmail(email,'email_db')
        print('Email sent to ',email.getReceiver())
        return
    else:
        return test1()

#test1()