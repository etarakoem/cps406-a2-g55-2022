import unittest
from account import UserAccount

class MyTestCase(unittest.TestCase):
    def test_regist(self):
        acc = UserAccount()
        #acc.account_file_reset()
        acc.file_reset('account_list')
        acc.file_reset('user_list')
        # Generate random 100 files
        with open('test_userName','r') as f:
            userList = f.read().split("\n")
        with open('test_Password', 'r') as f:
            passList = f.read().split("\n")
        with open('test_phone', 'r') as f:
            phoneList = f.read().split("\n")
        with open('test_name', 'r') as f:
            nameList = f.read().split("\n")
        with open('test_address','r') as f:
            addressList = f.read().split("\n")
        for i in range(len(userList) - 8):
            acc.regist(userList[i],userList[i] + "@example.com",passList[i],nameList[i],"Member",phoneList[i],addressList[i])
        for i in range(len(userList) - 8,len(userList)):
            acc.regist(userList[i], userList[i] + "@example.com", passList[i], nameList[i], "Coach", phoneList[i],addressList[i])
        score = 0
        for i in range(len(userList)):
            self.assertEqual(acc.checkExist(userList[i]), True)
            if acc.checkExist(userList[i]):
                score += 1

        print("Final score: ",score,"/",len(userList))


if __name__ == '__main__':
    unittest.main()
