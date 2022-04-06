from account import UserAccount
from clubEmailRecord import Email

class Admin(UserAccount):
    def options(self):
        mailBox = self.fetchMail(self.getEmail())
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
        # elif command == "5":
        #    self.enroll()
        elif command == "q":
            exit()
        else:
            print("Invalid option, please try again")
        return self.adminOptions()

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
