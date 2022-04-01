import sqlite3

# Author : Daniel Nigussie Gashaw
# This is class is designed to operate different database operations. The motivation comes from the different SQL commands that I can't remember when I try to
# on the database related progrmming. And one of the basic concepts of programming , in my opinion, is to make your and others programming life easier. Plus I 
# want to know and show others that how object oriented programming is so much easeir and fun to work with other than the structural programming. The name
# simpleDatabase is came up from its simplicity and simple operations. It might not be the perfect class but the idea is here and anyone who wants to modify it 
# and add new feature to it is always welcome. It is reusable and may be called so many times in the same or different programs. The author name should always
# needs to included wheather you modify it or use it as it is. For how to use the class read documentation.txt file


class simpleDatabase :
    def __init__(self):
        self.__databaseName = ''
        self.__cur = ''
        self.__conn = ''
        self.__tableName = ''
        self.__columnNames = []
        self.__dataTypes = []

    # The databaseName is a string
    def createDatabase(self,fullPath):
        path = self.__getPath(fullPath)
        try:
            self.__conn = sqlite3.connect(path)
            self.__cur =self.__conn.cursor()
        except :
            raise RuntimeError('Uanble to create the database')

    # Both the fullPath and databaseName are string variables
    def openDatabase(self,fullPath):
        
        path = self.__getPath(fullPath)

        try:
            self.__conn = sqlite3.connect(path)
            self.__cur = self.__conn.cursor()
        except :
            raise RuntimeError('Unable to open the path '+str(path))

    def __getPath(self,fullPath):

        pathList = []
        pathList = str(fullPath).split('\\')
        self.__databaseName = str(pathList[-1])
        path = ''

        if '.db' not in self.__databaseName:
            self.__databaseName = self.__databaseName + '.db'
        for item in pathList[:-1]:
            path = path+str(item)+'\\'
        path = path+self.__databaseName

        return path


    def getCursor(self):
        return self.__cur

    def getConnection(self):
        return self.__conn

    # The tbName is string, coulumnNmes and columnDataTypes are python list
    def createTable(self,tbName,columnNames,columnDataTypes,uniqueTableColumns):
        columnInfo = []
        userInput  = ''
        sqlCmdPart = ''
        uniqueCmdPart = ''
        self.__columnNames = columnNames
        self.__dataTypes = columnDataTypes
        i = 0
        self.__tableName = tbName
        sqlCmd = 'CREATE TABLE IF NOT EXISTS '+self.__tableName+' ('

        for i in range(len(columnNames)):
            dataType = str(columnDataTypes[i]).upper()
            userInput = columnNames[i]+' '+dataType
            columnInfo.append(userInput)

        sqlCmdPart = self.__concatenate(columnInfo)
        uniqueCmdPart = self.__concatenate(uniqueTableColumns)
        print (sqlCmdPart)
        print (uniqueCmdPart)

        if len(uniqueTableColumns) != 0:
            
            sqlCmd = sqlCmd + sqlCmdPart + ' , UNIQUE ('+uniqueCmdPart+ ' ) )'
        else:
            sqlCmd = sqlCmd+sqlCmdPart+' )'

        try:
            self.__cur.execute(sqlCmd)
        except RuntimeError as e:
            return e.message

    def getTableName(self):
        return self.__tableName
    def getDatabaseName(self):
        return self.__databaseName

    # A private method used by class members and its main purpose is to generate an insert command;
    # and tableName in this case is string and columnNames is a python string and return the variable sqlCmd an abbrivation for
    # SQL Command to its caller
    def __generateInsertCommand(self,tableName,columnNames):
        self.__tableName = tableName
        self.__columnNames = columnNames
        columnNames = ''
        valuePart = ''
        i = 0
        j = len(self.__columnNames)

        for item in self.__columnNames:
            questionMark = '?'
            if j != 1:
                item = item+' ,'
                questionMark = questionMark+' ,'
            columnNames = columnNames+item
            valuePart = valuePart+questionMark
            j-=1

        sqlCmd = 'INSERT INTO '+self.__tableName+' ( '+columnNames+' ) '+' VALUES '+'( '+valuePart+' )'

        return sqlCmd
    # Peivate member function. Its purpose to concatenate strings to create an SQL command that we need to oeprate on the database.
    # So this member function not need to be modify in anyway. 
    def __concatenate(self,listValue):
        listString = ''
        j = len(listValue)

        for item in listValue:
            if j != 1:
                item = item+' ,'
            listString = listString+item
            j -= 1

        return listString

    # The main purpose of this member function is to insert data to the table of the database. In this case,
    # the insrtedTuple is the tuple of the data needs to be inserted in the table, tableName is a simple string, and
    # columnName is a python list that contain the table column names that is\are going to be inserted to.
    def insertData(self,insertedTuple,tableName,columnNames):
        sqlCmd = self.__generateInsertCommand(tableName,columnNames)
        try:
            self.__cur.execute(sqlCmd, insertedTuple)
            self.__conn.commit()
        except RuntimeError as e:
            return e.message

    # The main purpose of this member function is to search items in the table of the database. In this 
    # case all the parameters are python strings. The SearchData should be the item in the tabel's columnName
    def searchData(self,tableName,columnName,searchData):
        i = 0
        result = []
        self.__tableName = tableName
        searchResult = []
        sqlCmd = 'SELECT * FROM '+self.__tableName+' WHERE '+columnName+' = ?'
        
        try:
            self.__cur.execute(sqlCmd,(searchData,))
            result = self.__cur.fetchall()

        except RuntimeError as e:
            return e.message
        if len(result) != 0:
            for i in range(len(result[0])):
                searchResult.append(result[0][i])
            return searchResult
        else:
            errorMsg = ' Can not find '+searchData+' in the '+tableName+' table.'
            return errorMsg

    def getTableData(self,tableName):

        tableData = []
        self.__tableName = tableName

        sqlCmd = 'SELECT * FROM '+self.__tableName
    
        #sqlCmd = 'SELECT * FROM '+self.__tableName+' ORDER BY '+str(orderBy)

        self.__cur.execute(sqlCmd)
        tableData = self.__cur.fetchall()

        return tableData

    def getColumnData(self,tableName,columnName):

        sqlCmd = ''
        columnData = []
        self.__tableName = tableName
        try:
            sqlCmd = 'SELECT '+columnName+' FROM '+self.__tableName 
            self.__cur.execute(sqlCmd)
            columnData = self.__cur.fetchall()

        except RuntimeError as e:
            return e.message

        return columnData

    # This function will update the whole column of a certain table with updateValue. In this case tableName and columnName are simple
    #python strings. While updateValue is a python tuple. If the function returns 1 means update went sucessfully otherwise it returns 0
    def updateColumn(self,tableName,columnName,updateValue):
        self.__tableName = tableName
        tbData = self.getTableData(tableName)

        sqlCmd = ''
        sqlCmd = 'UPDATE '+self.__tableName+' SET '+columnName+'=?'
        i = 0
        for item in updateValue:
            try :
                self.__cur.execute(sqlCmd,(updateValue[i],))
                self.__conn.commit()
                i+=1
                return 1
            except :
                raise RuntimeError
                return 0

    # This member function will delete or drop table name tbName if it exists in the database. In this case tbName is a simple python string
    def deleteTable(self,tbName):
        try :
            sqlCmd = 'DELETE TABLE IF EXISTS '+tbName
            self.__cur.execute(sqlCmd)

        except RuntimeError as e :
            return e.message


    # This member function will delete a single row if the itemToBeDeleted found in the columnName. In such cases all parameters are simple python strings.
    def deleteRow(self,tbName,itemToBeDeleted,columnName):
        sqlCmd = 'DELETE FROM '+str(tbName)+' WHERE '+str(columnName)+' = ?'

        try:
            self.__cur.execute(sqlCmd,(itemToBeDeleted,))
            self.__conn.commit()

        except RuntimeError as e:
            return e.message



    def closeDatabase(self):
        self.__conn.close()

    def __str__(self):
        return 'A database named '+str(self.__databaseName)
