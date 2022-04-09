import simpleDatabase as sd


class Transaction:
    def __init__ (self): # tType: str , amount: float, date: str,comment: str
        self.transactionType = ""
        self.amount = 0.0
        self.date = ""
        self.comment =""
        self.payee = ""
        
    
        
    def transaction(self,tType: str, amount: float, date: str, comment : str, payee: str):
        self.transactionType = tType
        self.amount = amount
        self. date = date
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
