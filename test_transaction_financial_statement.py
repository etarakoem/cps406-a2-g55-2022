import datetime
import simpleDatabase
import os

class Transaction:
    transaction_number = 17
    def __init__ (self): # tType: str , amount: float, date: str,comment: str
        self.transactionType = ""
        self.amount = 0.0
        self.date = ""
        self.comment =""
        self.payee = ""
   
        
   
        
    def transaction(self,tType: str, amount: float, date: str, comment : str, payee: str):
        self.transactionType = tType
        self.amount = amount
        self. date = self.date
        self.comment = comment
        self.payee = payee
        
    def get_trasnaction_type(self):
        return self.transactionType
    
    def get_transaction_amount(self):
        return self.amount
    
    def get_tranasction_date(self):
        return self.date
    
    def get_remarks(self):
        return self.comment
    
    def get_payee_name(self):
        return self.payee
    
    def get_receipt(self):
        return self.transactionType + "\n"+ "Customer Name: "+self.payee +"\n"+"Date of Transaction: " + self.date + "\n" + "Amount: $"+str(self.amount) +"\n" + "Reason for Payment: "+self.transactionType + "\n" + "Remarks: " + self.comment

class FinancialSatement:
    def __init__ (self, statementName: str, companyName: str, records: list):
        self.statementName = statementName
        self.companyName = companyName
        self.records = records
    
    def get_general_income_statement(self):
        expenses = {}
        date = [int(i) for i in ((self.records[0])[3]).split("-")]
        minDate = datetime.date(date[0], date[1],date[2])
        maxDate = minDate
        
        
        for item in self.records:
            dateRec = [int(i) for i in item[3].split("-")]
            newDate = datetime.date(dateRec[0], dateRec[1], dateRec[2])
            
            if newDate > maxDate:
                maxDate = newDate
            if newDate < minDate:
                minDate = newDate
        
        for item in self.records:
            if item[2] < 0:
                if item[4] not in list(expenses.keys()):
                    expenses[item[4]] = item[2]
                else:
                    expenses[item[4]] = expenses[item[4]] + item[2]
        
        income_statement ="\t\t\t\t\t\t"+self.companyName+ "\n"+"\t\t\t\t\tGeneral Income Statement\n"+ "\t\t\tFor the period of "+\
                          str(minDate)+" - "+str(maxDate)+"\n\n\n\nTotal Income --------------------------------------------   "\
                          +str(self.get_total_income()) +"\n\nExpenses:"+"\n\t\t"
                          
        keys_map = list(expenses.keys())
        
        i = 1
        for key in keys_map:
            income_statement = income_statement + str(i)+". "+key+"\t-------------------------- "+ str(expenses[key] *-1)+"\n\t\t"
            i = i + 1
        income_statement = income_statement + "\n\nTotal Expenses\t-----------------------------------------\t"\
            +str(self.get_total_expense() * -1) + "\n\nTotal Revenue\t-----------------------------------------  \t"\
                +str(self.get_total_income() + self.get_total_expense())
            
        return income_statement
        
    def get_total_income(self):
        totalIncome = 0
        for item in self.records:
            if item[2] > 0: 
                totalIncome = totalIncome + item[2]
        return totalIncome
            
    def get_total_expense(self):
        totalExpense = 0
        for item in self.records:
            if item[2] < 0:
                totalExpense = totalExpense + item[2]
        return totalExpense
    
    def __get_month_name(self, i):
        monthName = {"January": 1,  "February": 2, "March": 3, "April": 4 , "May": 5, "June":6, "July":7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        month_keys = monthName.keys()
        
        for key in month_keys:
            if monthName[key] == i:
                return key
    def get_monthly_income(self):
        
        monthlyIncome = {}
        for item in self.records:
            dateRec = [int(i) for i in item[3].split("-")]
            newDate = datetime.date(dateRec[0], dateRec[1], dateRec[2])
            
            month = newDate.month
            keyMonth = self.__get_month_name(month)
            
            if item[2] > 0:
                
                if keyMonth not in list(monthlyIncome.keys()):
                    monthlyIncome[keyMonth] = item[2]
                else :
                    monthlyIncome[keyMonth] = monthlyIncome[keyMonth] + item[2]
        return monthlyIncome
    
    def get_monthly_expense(self):
        
        monthlyIncome = {}
        for item in self.records:
            dateRec = [int(i) for i in item[3].split("-")]
            newDate = datetime.date(dateRec[0], dateRec[1], dateRec[2])
            
            month = newDate.month
            keyMonth = self.__get_month_name(month)
            
            if item[2] < 0:
                
                if keyMonth not in list(monthlyIncome.keys()):
                    monthlyIncome[keyMonth] = item[2]
                else :
                    monthlyIncome[keyMonth] = monthlyIncome[keyMonth] + item[2]
        return monthlyIncome
    
    def get_monthly_income_statement(self):
        
        
        monthlyIncome = self.get_monthly_income()
        monthlyExpense = self.get_monthly_expense()
        
        income_statement = "\t\t\t\t\t\t"+self.companyName+ "\n"+"\t\t\t\t\tMonthly Income Statement\n\n\n"
        
        incomeKey = monthlyIncome.keys()
        
        for key in incomeKey:
            income = monthlyIncome[key]
            expense = 0
            
            if key in list(monthlyExpense.keys()):
                expense = monthlyExpense[key] * -1
            
            income_statement = income_statement + key + "\n\t"+"Total Income\t--------------------\t"+str(income)+\
                "\n\tTotal Expense\t--------------------\t"+str(expense)+"\n\n\tTotal Revenue\t--------------------\t"+\
                    str(income - expense)+"\n\n"
        return income_statement
                

def record_income_trasaction(transaction: Transaction):
    currentWorkingDir = os.getcwd() 
    fileName = os.path.join(currentWorkingDir,"Transaction_Records.db")
    fileName = fileName.replace("\\", '/')
    db = sd.simpleDatabase()
    
    
    colNames = ["TransactionNumber", "Payee","Amount","Date", "TransactionType", "Remark" ]
    
    if (db.openDatabase(fileName) == None):
        db.createDatabase(fileName)
    
    else:   
        db.openDatabase(fileName)  
    
    if (db.getTableName() == None or db.getTableName() != "TransactionRecord"):
        db.createTable("TransactionRecord",colNames,["Integer","TransactionNumber","String", "Double", "String", "String", "String"], ["TransactionNumber"])
    
    
    
    db.insertData((Transaction.transaction_number,transaction.get_payee_name(), transaction.get_transaction_amount(), transaction.get_tranasction_date(),
                   transaction.get_trasnaction_type(),transaction.get_remarks()),"TransactionRecord", colNames)
    
    Transaction.transaction_number = Transaction.transaction_number + 1
    
    
    
    
def record_expense_transaction(transaction: Transaction):
    
    currentWorkingDir = os.getcwd() 
    fileName = os.path.join(currentWorkingDir,"Transaction_Records.db")
    fileName = fileName.replace("\\", '/')
    db = sd.simpleDatabase()
    db.createDatabase(fileName)
    db.openDatabase(fileName)
    
    colNames = ["TransactionNumber", "Payee","Amount","Date", "TransactionType", "Remark" ]
    db.createTable("TransactionRecord",colNames,["Integer","String", "Double", "String", "String", "String"], ["TransactionNumber"])
    
    db.insertData((Transaction.transaction_number,transaction.get_payee_name(), transaction.get_transaction_amount()*-1, transaction.get_tranasction_date(),
                   transaction.get_trasnaction_type(),transaction.get_remarks()),"TransactionRecord", colNames)
    
    Transaction.transaction_number = Transaction.transaction_number + 1
    
    #print(db.getTableData("TransactionRecord"))
    
    
def user_inputs(transaction: Transaction):
    transaction.payee = input("Enter payee name: ")
    transaction.amount = float(input("Enter the mount: "))
    transaction.date = input("Enter the date: ")
    transaction.transactionType = input("Enter the transaction type: ")
    transaction.comment = input("Enter a remark: ")

def get_general_financial_statement():
    currentWorkingDir = os.getcwd() 
    fileName = os.path.join(currentWorkingDir,"Transaction_Records.db")
    fileName = fileName.replace("\\", '/')
    db = sd.simpleDatabase()
    db.openDatabase(fileName)
    
    records = db.getTableData("TransactionRecord")
    
    fs = FinancialSatement("Income Statement", "Recreation Club", records)
    
    
    return fs.get_general_income_statement()
    
def get_monthly_financial_statement():
    currentWorkingDir = os.getcwd() 
    fileName = os.path.join(currentWorkingDir,"Transaction_Records.db")
    fileName = fileName.replace("\\", '/')
    db = sd.simpleDatabase()
    db.openDatabase(fileName)
    
    records = db.getTableData("TransactionRecord")
    
    fs = FinancialSatement("Income Statement", "Recreation Club", records)
    
    return fs.get_monthly_income_statement()
      
def main():
    Tran = Transaction()
    choice = 'y'
    user_input = 0
    
    
    while choice != 'n' : 
        print("================")
        print("Transaction Menu")
        print("================")
        print("1. Record Income")
        print("2. Record Expense")
        print("3. General Financial Statement")
        print("4. Monthly Financial Statement")
    
        user_input = input("Enter your choice: ")
        if user_input == "1":
            user_inputs(Tran)
            record_income_trasaction(Tran)
            #print(Tran.get_receipt())
        elif user_input == "2":
            user_inputs(Tran)
            record_expense_transaction(Tran)
            #print(Tran.get_receipt())
        elif user_input == "3":
           
            print(get_general_financial_statement())
        elif user_input == "4":
            print(get_monthly_financial_statement())
        
            
        choice = input("Would you like to enter another record? (y/n): ")
       
main()