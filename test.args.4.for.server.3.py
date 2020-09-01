import argparse
# https://pymotw.com/2/argparse/
parser = argparse.ArgumentParser()


parser.add_argument('-t', action='store', dest='simple_value',
                    help='type of database that do you want to use ej. MySQL SQLite')

parser.add_argument('-u', action='append', dest='collection_urls',
                    default=[],
                    help='Add repeated values to a list',
                    )

parser.add_argument('-f', action='append', dest='collection_files',
                    default=[],
                    help='Add repeated values to a list',
                    )


parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()



class MyClass2:
    def __init__(self, name,mytype):
        self.name = name
        self.lastname = None
        self.isURL = None
        self.isFILE = None
        self.tipo = mytype
        if mytype=="URL":
            self.isURL = True
            self.isFILE = False
            pass
        if mytype=="FILE":
            self.isFILE = True
            self.isURL = False
            pass
        else:
            pass
       #self.checkme = 'awesome {}'.format(self.name)

    def setName(self,name):
        self.lastname = name
        pass

    def getName(self):
        return self.name
    def pretty_print_name(self):
        print("This object's name is {}.".format(self.name))
        print("the path is {}.".format(self.name))
        print("the type is {}.".format(self.tipo))

    def pront(self):
        print("This object's name is {}.".format(self.lastname))
...

#instanceNames = ['red', 'green', 'blue']

# Here you use the dictionary
my_objects = []

print(my_objects)

#for i in range(5):
#    my_objects.append(MyClass(i))
for gg in results.collection_urls:
    print("URL",gg)
    my_objects.append({'PATH':gg,'TYPE':'URL'})
    pass


for gg in results.collection_files:
    print("FILE",gg)
    my_objects.append({'PATH':gg,'TYPE':'FILE'})
    pass

#my_objects =list(map(lambda x:x.pront(),my_objects))
# later

print("-")
print(my_objects)
print("-")
"""
for obj in my_objects:

    print(obj['URL'])
"""

holder = {MyClass2(gg['PATH'],gg['TYPE']) for gg in my_objects}

print(holder)
print("here we go")


for x in holder:
    x.pretty_print_name()