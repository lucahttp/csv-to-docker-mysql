import argparse
# https://pymotw.com/2/argparse/
parser = argparse.ArgumentParser()


parser.add_argument('-u', action='append', dest='collection_urls',
                    default=[],
                    help='Add repeated values to a list',
                    )

parser.add_argument('-p', action='append', dest='collection_files',
                    default=[],
                    help='Add repeated values to a list',
                    )


parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()


class MyClass:
    def __init__(self, name):
       self.name = name
       self.checkme = 'awesome {}'.format(self.name)
    def pretty_print_name(self):
        print("This object's name is {}.".format(self.name))
...

#instanceNames = ['red', 'green', 'blue']

# Here you use the dictionary
my_objects = []

print(my_objects)

#for i in range(5):
#    my_objects.append(MyClass(i))
for gg in results.collection_urls:
    print("URL",gg)
    my_objects.append(MyClass(gg))
    pass

# later

#print(my_objects)

for obj in my_objects:
    obj.pretty_print_name()

