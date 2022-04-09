import os.path

class textDB:
    def __init__(self):
        self.fileName = ''

    def fileName(self,name: str):
        currentWorkingDir = os.getcwd()
        fileName = os.path.join(currentWorkingDir, "emailDB.db")
        fileName = fileName.replace("\\", '/')
        return fileName

    def createDB(self,name: str):
        f = open(name,'x')
        f.close()

    def openDB(self,name: str):
        self.fileName = name

    def insert(self,content: str):
        with open(self.fileName,'a') as f:
            f.write(content+'\n')
        f.close()

    def remove(self,content: str):
        with open(self.fileName,'r') as f:
            lines = f.read().split('\n')
            rewrite = [line for line in lines if line != content]
            f.close()
        with open(self.fileName,'w') as f:
            for line in rewrite:
                f.write(line+'\n')
            f.close()

    def getFile(self):
        return self.fileName

    def retrieve(self,name: str):
        self.openDB(name)
        allMails = []
        with open(self.getFile(),'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                if line != '' or line != "":
                    section = line.split(":")
                    allMails.append(section)
        return allMails

    def rawRetrieve(self,name: str,requirement):
        self.openDB(name)
        allMails = []
        with open(self.getFile(), 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                if line != '' or line != "":
                    if requirement in line:
                        allMails.append(line)
        return allMails