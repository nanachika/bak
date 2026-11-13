import saving
import templates as tmp


class record(tmp.fields):
    def __init__(self, parent, name):
        super().__init__(holding(parent, name))


class struct(tmp.table):
    def __init__(self):
        super().__init__(record)  # type: ignore
        self.towns = towns()
        self.categories = categories()
        self.products = products()

    def add(self, parent, name):
        self.things.append(self.field(parent, name))  # type: ignore

    def addCategory(self, name):
        if not self.categories.find(name):
            self.categories.add(name)

    def addProduct(self, name, category):
        self.addCategory(category)
        self.products.add(name, category)

    def printCategories(self):
        self.categories.print()

    def printProducts(self):
        self.products.print()

    def printTowns(self):
        self.towns.print()

    def printStores(self, twn=''):
        for i in self.things:
            print(i.name.name)
            i.name.printStores(3)

    def printHaving(self, twn=''):
        for i in self.things:
            if i.name.verifyHaving():
                print(i.name.name)
                i.name.printHaving(twn)

    def save(self, file):
        #stores.txt
        s = []
        file.setName('stores.txt')
        file.open('w')
        for i in self.things:
            hld = i.name
            s.append('[' + hld.name + ']\n')
            for st in hld.stores.things:
                s.append(st.getTown() + ',' + st.getAddress() + '\n')
        file.writes(s)
        file.close()

        #products.txt
        s = []
        file.setName('products.txt')
        file.open('w')
        for cat in self.categories.things:
            cat_name = cat.getName()
            s.append('[' + cat_name + ']\n')
            for prod in self.products.things:
                if prod.getCategory() == cat_name:  # type: ignore
                    s.append(prod.getName() + '\n')
        file.writes(s)
        file.close()

        #having.txt
        s = []
        file.setName('having.txt')
        file.open('w')
        for i in self.things:
            hld = i.name
            if hld.verifyHaving():
                s.append('[' + hld.name + ']\n')
                for item in hld.having.things:
                    line = f"{item.town},{item.address},{item.category},{item.product},{item.count},{item.price}\n"
                    s.append(line)
        file.writes(s)
        file.close()

    def find(self, name):
        for i in self.things:
            if i.name.name == name:
                return i.name
        return None

    def read(self, file):
        file.setName('stores.txt')
        file.open()
        hldng = None
        while (s := file.read()):
            s = s.strip()
            if not s:
                continue
            if s[0] == '[':
                h_name = s[1:-1]
                self.add(self, h_name)
                hldng = self.find(h_name)
            else:
                parts = s.split(',', 1)
                if hldng:
                    hldng.addStore(parts[0].strip(), parts[1].strip())
        file.close()

        file.setName('products.txt')
        file.open()
        category = ''
        while (s := file.read()):
            s = s.strip()
            if not s:
                continue
            if s[0] == '[':
                category = s[1:-1]
                self.addCategory(category)
            else:
                self.addProduct(s, category)
        file.close()

        file.setName('having.txt')
        file.open()
        hldng = None
        while (s := file.read()):
            s = s.strip()
            if not s:
                continue
            if s[0] == '[':
                h_name = s[1:-1]
                hldng = self.find(h_name)
                if not hldng:
                    self.add(self, h_name)
                    hldng = self.find(h_name)
            else:
                parts = [p.strip() for p in s.rsplit(',', 4)]
                town_addr = parts[0].split(',', 1)
                if hldng:
                    hldng.addHave(town_addr[0].strip(), town_addr[1].strip(), parts[1], parts[2], parts[3], parts[4])
        file.close()


class holding():
    def __init__(self, parent, name='Рога и копыта'):
        self.name = name
        self.stores = stores()
        self.parent = parent
        self.having = having()

    def addStore(self, town, address):
        self.addTown(town)
        if not self.stores.find(town, address):
            self.stores.add(town, address)

    def addTown(self, name):
        if not self.parent.towns.find(name):
            self.parent.towns.add(name)

    def printStores(self, left=0):
        self.stores.print(left)

    def addHave(self, town, address, category, product, count, price):
        if not self.stores.find(town, address):
            self.addStore(town, address)
        if not self.parent.products.find(category, product):
            self.parent.addProduct(product, category)
        self.having.add(town, address, category, product, count, price)

    def printHaving(self, town):
        self.having.print(town)

    def verifyHaving(self):
        return len(self.having.things) > 0

    def saveStores(self):
        return self.stores.save()

    def saveHaving(self):
        return self.having.save()


class town(tmp.fields):
    def __init__(self, name):
        super().__init__(name)


class towns(tmp.table):
    def __init__(self):
        super().__init__(town)


class stores(tmp.table):
    def __init__(self):
        super().__init__(store)  # type: ignore

    def add(self, town, address):
        self.things.append(self.field(town, address))  # type: ignore

    def print(self, left=0):
        for i in self.things:
            print(left * ' ' + f'{i.getTown()} {i.getAddress()}')  # type: ignore

    def find(self, town, address):
        for i in self.things:
            if i.getTown() == town and i.getAddress() == address:  # type: ignore
                return True
        return False

    def save(self):
        s = []
        for i in self.things:
            s.append(f'{i.getTown()},{i.getAddress()}\n')  # type: ignore
        return s


class store(tmp.fields):
    def __init__(self, town, address):
        super().__init__(address)
        self.town = town

    def getTown(self):
        return self.town

    def getAddress(self):
        return self.name


class category(tmp.fields):
    def __init__(self, name):
        super().__init__(name)


class categories(tmp.table):
    def __init__(self):
        super().__init__(category)


class products(tmp.table):
    def __init__(self):
        super().__init__(product)  # type: ignore

    def add(self, name, category):
        self.things.append(self.field(name, category))  # type: ignore

    def print(self):
        for i in self.things:
            print(f'{i.getName()} {i.getCategory()}')  # type: ignore

    def find(self, category, product):
        for i in self.things:
            if i.getCategory() == category and i.getName() == product:  # type: ignore
                return True
        return False


class product(tmp.fields):
    def __init__(self, name, category):
        super().__init__(name)
        self.category = category

    def getCategory(self):
        return self.category


class have():
    def __init__(self, town, address, category, product, count, price):
        self.town = town
        self.address = address
        self.category = category
        self.product = product
        self.count = count
        self.price = price


class having(tmp.table):
    def __init__(self):
        super().__init__(have)  # type: ignore

    def add(self, town, address, category, product, count, price):
        self.things.append(self.field(town, address, category, product, count, price))  # type: ignore

    def print(self, town):
        for i in self.things:
            if i.town == town or town == '':
                print(f'   {i.town}, {i.address}, {i.category}, {i.product}, {i.count}, {i.price}')

    def save(self):
        s = []
        for i in self.things:
            s.append(f'{i.town},{i.address},{i.category},{i.product},{i.count},{i.price}\n')
        return s


f = saving.file()

t = struct()
t.read(f)

while True:
    cmd = input('Введите команду: ')
    if cmd == 'exit':
        break
    elif cmd == 'addTown':
        name = input('Введите имя: ')
        if not t.towns.find(name):
            t.towns.add(name)
    elif cmd == 'addStore':
        name = input('Введите название сети (холдинга): ')
        twn = input('Введите город: ')
        addrss = input('Введите адрес: ')
        hld = t.find(name)
        if not hld:
            t.add(t, name)
            hld = t.find(name)
        if hld:
            hld.addStore(twn, addrss)
    elif cmd == 'printTowns':
        t.printTowns()
    elif cmd == 'printStores':
        t.printStores()
    elif cmd == 'addCategory':
        name = input('Введите имя: ')
        t.addCategory(name)
    elif cmd == 'addProduct':
        name = input('Введите имя: ')
        ctgr = input('Введите категорию: ')
        t.addProduct(name, ctgr)
    elif cmd == 'printCategories':
        t.printCategories()
    elif cmd == 'printProducts':
        t.printProducts()
    elif cmd == 'addHaving':
        nm = input('Введите название сети (холдинга): ')
        twn = input('Введите город: ')
        addrss = input('Введите адрес: ')
        ctgr = input('Введите категорию: ')
        prdct = input('Введите продукт: ')
        cnt = input('Введите количество: ')
        prc = input('Введите цену: ')
        hld = t.find(nm)
        if not hld:
            t.add(t, nm)
            hld = t.find(nm)
        if hld:
            hld.addHave(twn, addrss, ctgr, prdct, cnt, prc)
    elif cmd == 'printHaving':
        twn = input('Введите город: ')
        t.printHaving(twn)
    elif cmd == 'save':
        t.save(f)