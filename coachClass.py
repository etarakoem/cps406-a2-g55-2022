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

    def quickOptions(self,command,email = Email()):
        mailBox, mail_count = self.print_Options()
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
        elif command == "q":
            return
        else:
            print("Invalid option, please try again")
            return self.options()
        return self.options()
    def options(self):
        self.print_Options()
        print("5) Register a new club")
        print("6) Make an announcement")
        print("7) Send an email")
        print("8) Add Member")
        command = input("What would you like to do today? ")
        return self.quickOptions(command)

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

    def addMember(self):
        pass

    def addMemberMailing(self,member,mailing):
        with open('memberMailingList','a') as f:
            f.write(f'{member}:{mailing}')
            f.close()

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

def testMakeClub():
    acc = Coach()
    acc.login('sarah','batman')
    #acc.quickOptions("5")
    acc.coachAnnounceForTesting()

#testMakeClub()
