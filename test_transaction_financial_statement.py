import transaction.Transaction
import financial_statement.FinancialSatement
import os

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
    
    
    return fs.get_general_income_statement()
    
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
      