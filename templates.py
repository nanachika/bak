class fields():
    def __init__(self,name):
        self.name=name
        
    def getName(self):
        return self.name

class table():
    def __init__(self,field: type[fields]):
        self.things=[]
        self.field=field

    def add(self,name):
        self.things.append(self.field(name))

    def print(self):
        for i in self.things:
            print(f'{i.getName()}')

    def find(self,name):
        for i in self.things:
            if i.getName()==name:
                return True
        return False