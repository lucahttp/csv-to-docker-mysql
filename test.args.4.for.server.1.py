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

for gg in results.collection_urls:
    print("URL",gg)
    pass

class MyClass:
   def __init__(self, name):
       self.name = name
       self.checkme = 'awesome {}'.format(self.name)
...

instanceNames = ['red', 'green', 'blue']

# Here you use the dictionary
holder = {name: MyClass(name=name) for name in results.collection_urls}




print(holder)

for x in holder:
    print(holder[x]) 
    print(holder[x].checkme)