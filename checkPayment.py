import simpleDatabase as sd
import os
class PaymentHistory:

    def getMemberList(self):
        currentWorkingDir = os.getcwd() 
        fileName = os.path.join(currentWorkingDir,"Transaction_Records.db")
        fileName = fileName.replace("\\", '/')
        db = sd.simpleDatabase()
        db.createDatabase(fileName)
        db.openDatabase(fileName)
        colNames = ["TransactionNumber", "Payee","Amount","Date", "TransactionType", "Remark" ]
        db.createTable("TransactionRecord",colNames,["Integer","String", "Double", "String", "String", "String"], ["TransactionNumber"])
        membersList = db.getTableData("TransactionRecord")
        return membersList
        
    def getPaidMembers(self):
        membersList = self.getMemberList()
        paidMembers = []
        i = 0
        for item in membersList:
            if item[2] > 0:
                paidMembers.insert(i, item[1])
                i += 1
        return paidMembers

    def getUnpaidMembers(self):
        membersList = self.getMemberList()
        unPaidMembers = []
        i = 0
        for item in membersList:
            if item[2] == None:
                unPaidMembers.insert(i, item[1])
                i += 1
        if (len(unPaidMembers) == 0):
            return 
        else:
            return unPaidMembers
