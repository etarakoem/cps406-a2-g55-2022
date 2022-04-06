from clubEmailRecord import Email

class UserAccount(object):

    def __init__(self):
        self.username = 'Admin'
        self.password = 'admin'
        self.name = 'Admin'
        self.email = 'Username@example.com'
        self.role = 'Admin'
        self.phone = '0123456789'
        self.address = 'my home'
        self.club = 'club_List'
        self.mailbox = "email_db"
        self.accountList = 'account_list'
        self.userList = 'user_list'

    def loginAs(self,username,passwd,email,name,role,phone,address):
        self.setName(name)
        self.setPass(passwd)
        self.setRole(role)
        self.setEmail(email)
        self.setUser(username)
        self.setPhone(phone)
        self.setAddress(address)

    def fetchMail(self,username):
        # Error, needs implement again or find a better solution
        mail = Email()
        return mail.findMailsOf('email_db',username)

    def user_base_dump(self):
        print(f'{"Account":20} \t {"email":25} \t {"name":20} \t {"role":20} \t {"phone":20} \t {"address":20}')
        with open(self.accountList,'r') as f:
            data = f.read().split("\n")
            for i in data:
                account = i.split(":")
                print(f'{account[0]:20} {account[2]:25} {account[3]:20} {account[4]:20}  {account[5]:20} \t {account[6]:20}')
        return

    def allEmail(self):
        print(f'{"email":25} \t {"name":20} \t {"role":20}')
        with open(self.accountList, 'r') as f:
            data = f.read().split("\n")
            for i in data:
                account = i.split(":")
                print(f'{account[2]:25} \t {account[3]:20} \t {account[4]:20}')
        return

    def sendEmail(self):
        email = Email()
        print("Sending email: ")
        if self.getRole() == 'Admin':
            print("0) View all accounts info")
        print("1) View all emails address can be sent")
        print("2) Sending email")
        command = input("> ")
        if command == "0" and self.getRole() == 'Admin':
            self.user_base_dump()
        elif command == "1":
            self.allEmail()
        elif command == "2":
            email.setSender(self.getEmail())
            email.compose()
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

    def viewClub(self,username):
        clubList = []
        with open(self.club) as f:
            clubs = f.read().split("\n")
            for club in clubs:
                section = club.split(':')
                name = section[1]
                if name == username:
                    clubList.append(section[0])
        return clubList

    def annouceToClub(self):
        clubs = self.viewClub(self.getUser())
        if len(clubs) == 0:
            print("You haven't declare any club")
            return
        else:
            print("Club no. \t|\tClub names")
            for i in range(len(clubs)):
                print(i + "\t|\t" + clubs[i])

    def viewMail(self,mails):
        print("ID\t|\tTitle")
        for i in range(len(mails)):
            print(i+"\t|\t"+mails[i][0])

        command = input("View mail number: ")
        print('From:\t' + mails[command][1])
        print(mails[command][2])

        command = input("Enter R to return to email list, M to return to menu")
        if command == "r" or command == "R":
            return self.viewMail(mails)

        return

    def print_Options(self):
        mailBox = self.fetchMail(self.getUser())
        print("Menu: ")
        mail_count = len(mailBox)
        if mail_count > 0:
            print("You got ", mail_count, " mail")
            print("0) view Mailbox")
        print("1) Change password")
        print("2) Change email")
        print("3) Change phone number")
        print("4) Change name")

    def admin_setUser(self):
        username = input('Which user would you like to change?')
        if username == 'q':
            exit(0)
        if self.checkExist(username):
            password = self.accountLookup(username,1)
            self.login(username,password)
            role = input('Changing role from '+self.getRole()+' into: ')
            self.setRole(role)
            self.updateAccount()
            self.login('admin','admin')
        else:
            print('Username does not exist')
            return self.admin_setUser()

    def adminOptions(self):
        mailBox = self.fetchMail(self.getName())
        print("Menu: ")
        print(len(mailBox))
        mail_count = len(mailBox)
        if mail_count > 0:
            print("You got ", mail_count, " mail")
            print("0) view Mailbox")
        print("1) Lookup coach list")
        print("2) lookup member list")
        print("3) Change user status")
        print("4) send an Email")
        command = input("What would you like to do today?, Q to quit\n")
        if command == "0" and mail_count > 0:
            self.viewMail(mailBox)
        elif command == "1":
            self.listAllMember('Coach')
        elif command == "2":
            self.listAllMember('Member')
        elif command == "3":
            self.admin_setUser()
        elif command == "4":
            self.sendEmail()
        #elif command == "5":
        #    self.enroll()
        elif command == "q":
            exit()
        else:
            print("Invalid option, please try again")
        return self.adminOptions()


    def coachOptions(self):
        mailBox = self.fetchMail(self.getUser())
        mail_count = len(mailBox)
        self.print_Options()
        print("5) Register a new club")
        print("6) Make an announcement")
        print("7) Send an email")
        command = input("What would you like to do today? ")
        if command == "0" and mail_count > 0:
            self.viewMail(mailBox)
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
            return self.coachOptions()
        return self.coachOptions()

    def memberoptions(self):
        mailBox = self.fetchMail(self.getUser())
        mail_count = len(mailBox)
        self.print_Options()
        print("5) Enroll in a club")
        print("6) Pay")
        print("7) View unpaid club")
        print("")
        command = input("What would you like to do today? ")
        if command == "0" and mail_count > 0:
            self.viewMail(mailBox)
        elif command == "1":
            self.changePassword()
        elif command == "2":
            self.changeEmail()
        elif command == "3":
            self.changePhone()
        elif command == "4":
            self.changeName()
        elif command == "5":
            self.enroll()
        elif command == "q":
            return
        else:
            print("Invalid option, please try again")
            return self.memberoptions()
        return self.memberoptions()

    def options(self):
        role = self.getRole()
        if role == "Member":
            return self.memberoptions()
        elif role == "Coach":
            return self.coachOptions()
        elif role == "Admin":
            return self.adminOptions()

    def login(self,username,passwd):
        if not self.checkExist(username):
            print("Account not exist")
            return False
        with open("account_list",'r') as f:
            accounts = f.read().split("\n")
            for account in accounts:
                each = account.split(":")
                if username == each[0]:
                    if passwd == each[1]:
                        self.loginAs(username,passwd,each[2],each[3],each[4],each[5],each[6])
                        return self
                    else:
                        print('Login Failed')
                        return False
        return True

    def changeAddress(self):
        address = input("Type your new Password: ")
        self.setAddress(address)
        self.updateAccount()
        return

    def changePassword(self):
        password = input("Type your new Password: ")
        self.setPass(password)
        self.updateAccount()
        return

    def changeEmail(self):
        email = input("Type your new email: ")
        self.setEmail(email)
        self.updateAccount()
        return

    def changePhone(self):
        phone = input("Type your new phone number: ")
        self.setPhone(phone)
        self.updateAccount()
        return

    def changeName(self):
        name = input("Type your new name: ")
        self.setName(name)
        self.updateAccount()
        return


    def updateAccount(self):
        """
        Rewrite the whole database then re register the account
        """
        username = self.getUser()
        passwd = self.getPassword()
        email = self.getEmail()
        name = self.getName()
        role = self.getRole()
        phone = self.getPhone()
        address = self.getAddress()
        self.removeAccount(username)
        self.regist(username,email,passwd,name,role,phone,address)


    def removeAccount(self,username):
        with open("account_list", 'r') as f:
            accounts = f.read().split("\n")
        with open("account_list", "w") as f:
            for i in range(len(accounts)):
                each = accounts[i].split(":")
                if each[0] != username and i != len(accounts):
                    f.write(accounts[i]+"\n")
                elif each[0] != username and i == len(accounts):
                    f.write(accounts[i])
            f.close()
        with open("user_list", 'r') as f:
            users = f.read().split("\n")
        with open("user_list", 'w') as f:
            for i in range(len(users)):
                if users[i] != username and i != len(users):
                    f.write(users[i]+"\n")
                elif users[i] != username and i == len(users):
                    f.write(users[i])
        return


    def regist(self, username,email, passwd, name, role, phone,address):
        content = username + ":" + passwd + ":" + email + ":" + name + ":" + role + ":" + phone + ":" + address + "\n"
        self.addToFile("account_list",content)
        self.addToFile("user_list", username+"\n")

    def userRegist(self):
        username = input("Make a new username: ")
        if self.checkExist(username):
            command = input("Username exist. Try again? y/N ")
            if command == 'y' or command == 'Y':
                return self.userRegist()
            else:
                exit(0)
        password = input("Make a new password: ")
        name = input("What's your name?")
        phone = input("Your phone number: ")
        address = input("Please provide your address")
        email = input("Please provide your email")
        return self.regist(username,email,password,name,"Member",phone,address)


    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name
        return

    def setPass(self,password):
        self.password = password

    def getPassword(self):
        return self.password

    def getAddress(self):
        return self.address

    def setAddress(self,address):
        self.address = address

    def checkExist(self, username):
        with open("user_list", 'r') as f:
            content = f.read()
            if username in content:
                return True
        return False

    def addToFile(self, whichFile,content):
        with open(whichFile,"a") as f:
            f.write(content)
        return 0

    def getEmail(self):
        return self.email

    def setEmail(self,email):
        self.email = email
        return

    def setRole(self,role):
        self.role = role
        return

    def getRole(self):
        return self.role

    def getUser(self):
        return self.username

    def setUser(self,username):
        self.username = username
        return

    def setPhone(self,phone):
        self.phone = phone
        return

    def getPhone(self):
        return self.phone

    def summaryPage(self):
        print("Greetings, ", self.getName(),"(",self.getRole(),")")
        print("Your email: ", self.getEmail())
        print("Your Phone number: ", self.getPhone())
        print("Your current Address: ", self.getAddress())

    def coachAddMember(self,club):
        with open(self.club,'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                section = line.split(':')
                if self.getUser() == section[1] and club == section[0]:
                    return True
        return False

    def addClub(self,club):
        with open('club_List','a') as f:
            f.write("\n"+club + ":" + self.getUser() + ":" + self.getName())
        f.close()

    def userID_to_Type(self,username,type):
        with open('account_list','r') as f:
            names = f.read().split("\n")
            for name in names:
                section = name.split(":")
                if section[0] == username:
                    return section[type]
        print("Username "+username+" not found")
        return

    def type_to_userID(self,type,name):
        with open(self.accountList,'r') as f:
            accounts = f.read().split("\n")
            for account in accounts:
                if account[type] == name:
                    return account[0]

    def enroll(self):
        club_name = []
        instructor = []
        print("Club ID \t| Club name \t| Instructor")
        with open('club_List','r') as f:
            clubs = f.read().split("\n")
            for i in range(len(clubs)):
                club = clubs[i].split(":")
                club_name.append(club[0])
                instructor.append(club[2])
                print(i,"\t| ",club[0],"\t| ",club[2])
            command = int(input("which club would you like to enroll?"))
            print("Enroll in " + club_name[command] +" by instructor: " + instructor[command])

    def coachMenu(self):
        if self.getRole() != 'Coach':
            print('You need to be the coach to access this menu')
            return

    def file_reset(self,refile):
        with open(refile, 'w') as f:
            f.write("")
            f.close()



