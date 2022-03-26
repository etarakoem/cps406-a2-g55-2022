"""
    author: Phuc Hua
    This is just a user interaction python file.
"""
from account import UserAccount
class Function(object):

    def createAccount(self,role):
        acc = UserAccount()
        username = input("Username: ")
        if not acc.checkExist(username):
            password = input("Password: ")
            email = input("Email: ")
            name = input("Your name: ")
            phone = input("Phone number: ")
            acc.regist(username,email, password, name, role,phone)
        else:
            print("User already Exist, please try again")
            self.createAccount(role)
            return 0
        return 0


    def userSection(self):
        acc = UserAccount()
        username = input("Username: ")
        password = input("Password: ")
        if username == "" or password == "":
            print('Invalid input')
            return self.userSection()
        status = acc.login(username,password)
        if not status:
            command = input("Login again? y/N ")
            if command == 'y' or command == 'Y':
                return self.userSection()
            else:
                print("Good Bye")
                exit()
        print('Login Successfully as: ', acc.getName())
        acc.summaryPage()
        acc.options()
        return True

    def menu(self):
        print("Welcome to MEM")
        print("1) Login")
        print("2) Register an Account")
        command = input("Options:[1/2] ")
        if command == "1":
            return self.userSection()
        elif command == "2":
            acc = UserAccount
            return acc.userRegist()
        return 0