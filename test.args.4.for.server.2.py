import argparse
# https://pymotw.com/2/argparse/
# https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python
class MyClass:
    def __init__(self):
        self.name = None
        #self.pretty_print_name()

    def pretty_print_name(self):
        print("This object's name is {}.".format(self.name))

    def setNAME(self,gg):
        self.name = gg
        #print("This object's name is {}.".format(self.name))




instanceNames = ['red', 'green', 'blue']
my_objects = {}
diroftask = {}
"""
for i in instanceNames:
    #name = 'obj_{}'.format(i)
    name = i
    diroftask[name] = my_objects.get(MyClass().setNAME(name))
"""

holder = {MyClass().setNAME(gg) for gg in instanceNames}

print(holder)


for x in holder:
    print(holder[x]) 
    #print(my_objects[x].checkme)