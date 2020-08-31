# https://stackoverflow.com/questions/3182183/how-to-create-a-list-of-objects
class MyClass(object):
    def __init__(self, number):
        self.number = number
    def pretty_print_name(self):
        print("This object's name is {}.".format(self.number))
    def setNAME(self,gg):
        self.name = gg
        #print("This object's name is {}.".format(self.name))

my_objects = []

print(my_objects)

for i in range(5):
    my_objects.append(MyClass(i))

# later

#print(my_objects)

for obj in my_objects:
    obj.pretty_print_name()


#print(my_objects)
