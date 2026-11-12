class file():
    def __init__(self,fname='trest.txt'):
        self.fname=fname
        self.file=None
    def read(self):
        return self.file.readline()
    def setName(self,name):
        self.fname=name
    def write(self,s):
        self.file.write(s+'\n')
    def writes(self,s):
        self.file.writelines(s)
    def open(self,type='r'):
        self.file=open(self.fname,type,encoding='utf-8')
    def close(self):
        self.file.close()