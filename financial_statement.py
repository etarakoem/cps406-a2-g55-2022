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