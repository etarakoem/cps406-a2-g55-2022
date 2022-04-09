from account import UserAccount
from clubEmailRecord import Email
import textDatabase as td

class Coach(UserAccount):

    def coachAnnounceForTesting(self, mail = Email()):
        clubList = self.viewClub(self.getUser())
        for i in clubList:
            name = self.getName().replace(" ","_")
            club = i.replace(" ","_")
            clubname = name+"_"+club
            mail.anEmail(self.getEmail(),i,'Testing Email',f'Successfully send to {clubname}')
            mail.sendEmail(clubname)
        return

    def coachAnnounce(self):
        mail = Email()
        clubList = self.viewClub(self.getUser())
        if len(clubList) > 0:
            print("Available receiver:")
            for i in clubList:
                print(i)
            print('\n')
            mail.compose(self.getEmail())
        else:
            print("You haven't declare a club yet. No club to announce \nMaybe try to regist for a club?")
            command = input('Press Enter to continue... ')
        return

    def quickOptions(self,command,mailBox,mail_count,email = Email()):
        if command == "0" and mail_count > 0:
            email.viewMailOptions(mailBox)
        elif command == "1":
            self.changePassword()
        elif command == "2":
            self.changeEmail()
        elif command == "3":
            self.changePhone()
        elif command == "4":
            self.changeName()
        elif command == "5":
            clubName = input("What would your club called? ")
            self.addClub(clubName)
        elif command == "6":
            self.coachAnnounce()
        elif command == "7":
            self.sendEmail()
        elif command == "8":
            self.viewRequest()
        elif command == "q":
            return
        else:
            print("Invalid option, please try again")
            return self.options()
        return self.options()

    def options(self):
        mailBox, mail_count = self.print_Options()
        print("5) Register a new club")
        print("6) Make an announcement")
        print("7) Send an email")
        print('8) View Club Join request')
        command = input("What would you like to do today? ")
        return self.quickOptions(command,mailBox,mail_count)

    def clubMailingGenerate(self,club):
        name = self.getName().replace(" ","_")
        return f'{name}_{club.replace(" ","_")}'

    def addClub(self,club):
        club_mailing = self.clubMailingGenerate(club)
        with open('club_List','a') as f:
            # Database to reminds which coach own which Club mailing
            f.write(f"\n{club}:{self.getUser()}:{self.getName()}:{club_mailing}")
        f.close()
        # Create a new email db that anyone within this club will receive any notification from the code
        td.textDB().createDB(club_mailing)
        return

    def approveAll(self,email = Email(),db = td.textDB()):
        requestList = email.findMailWithContent('member_enroll_club', 'email_db', self.getEmail())
        print(requestList)
        for request in range(len(requestList)):
            section = requestList[request]
            self.addMemberMailing(section[1],self.clubMailingGenerate(section[3]))
        #Cleaning after adding to memberMailingList
        list = db.rawRetrieve('email_db','member_enroll_club')
        for i in list:
            #db.remove(i)
            pass
        return

    def viewRequest(self,email = Email()):
        requestList = email.findMailWithContent('member_enroll_club','email_db',self.getEmail())
        print(f"{'ID':8} | {'Name':25} | {'Email contact':25} | {'Club Joining':25}")
        for request in range(len(requestList)):
            section = requestList[request]
            print(f"{request:8} | {self.type_to_type(2,3,section[1]):25} | {section[1]:25} | {section[3]:25}")
        self.addMemberOptions()

    def addMemberOptions(self):
        print('1) Approve all ')
        print('2) Adding member manually')
        command = input('> ')
        if command == '1':
            return self.approveAll()
        else:
            print('Invalid input')
            return self.addMemberOptions()
        #self.addMemberMailing()

    def addMemberMailing(self,member,mailing,email = Email()):
        email.subscribe(member,mailing)

    def checkAvailableClub(self,club):
        if club in self.viewClub(self.getUser()):
            return True
        return False

    def coachAddMember(self,club,member,mailingList):
        if self.checkAvailableClub(club):
            if self.checkIfMemberInClub(member,club):
                with open('clubMember','a') as f:
                    f.write(f'{member}:{club}:{mailingList}')
                f.close()
        return

    def clubMemberRM(self,content):
        with open('clubMember','r') as f:
            lines = f.read().split('\n')
            contents = [line for line in lines if line != content]
            f.close()
        with open('clubMember','w') as f:
            for line in contents:
                f.write(line+"\n")
        return

    def coachRemoveMember(self, club, member):
        if self.checkAvailableClub(club):
            if self.checkIfMemberInClub(member, club):
                content = f'{member}:{club}:{self.getName()}'
                self.clubMemberRM(content)
        return

def testCoachMenu():
    acc = Coach()
    acc.login('sarah','batman')
    acc.options()
    #acc.quickOptions('0')
    #acc.options()
#testCoachMenu()

def testMakeClub(email = Email()):
    acc = Coach()
    mem = UserAccount()
    mem.login('kitty','meomeo')
    mem.quickOptions("")
    #mem.straightEnroll()
    mailBox,mail_count = acc.print_Options()
    acc.login('sarah','batman')
    acc.quickOptions("8",mailBox,mail_count)
    #acc.coachAnnounceForTesting()

#testMakeClub()
