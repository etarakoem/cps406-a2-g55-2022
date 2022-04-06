"""
    author: Phuc Hua
    This is just a user interaction python file.
"""
import account, coachClass, adminClass
class Function(object):

    def createAccount(self,role):
        acc = account.UserAccount()
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
        acc = account.UserAccount()
        username = input("Username: ")
        password = input("Password: ")
        if username == "" or password == "":
            print('Invalid input')
            return self.userSection()
        status = acc.login(username,password)
        if not status:
            command = input("Login again? y/N ")
            if command == 'y' or command == 'Y':
                return self.menu()
            else:
                print("Good Bye")
                exit()
        print('Login Successfully as: ', acc.getName())
        if acc.getRole() == 'Admin':
            acc = adminClass.Admin()
        elif acc.getRole() == 'Coach':
            acc = coachClass.Coach()
        acc.login(username,password)
        acc.summaryPage()
        acc.options()
        return True

    def userList(self,type):
        print(f'{"Username":25}{"Password":25}\n')
        with open('account_list','r') as f:
            lines = f.read().split('\n')
            for line in lines:
                section = line.split(':')
                if section[4] == type:
                    print(f'{section[0]:25} {section[1]:25}')
        print('\n')

    def menu(self):
        print("Welcome to MEM")
        print("1) Login")
        print("2) Register an Account")
        command = input("Options:[1/2] ")
        if command == "1":
            return self.userSection()
        elif command == "2":
            acc = account.UserAccount()
            return acc.userRegist()
        elif command == 'cl':
            self.userList('Coach')
            return self.menu()
        elif command == 'ml':
            self.userList('Member')
            return self.menu()
        else:
            print('Invalid input')
            return self.menu()
        return 0