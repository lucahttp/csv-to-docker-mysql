import argparse
# https://pymotw.com/2/argparse/
parser = argparse.ArgumentParser(description="Tool to keep archiving tar files")

group = parser.add_argument_group('some group')
group.add_argument("-a", "--action", dest="action", choices=("start", "stop", "list"), help="start/stop/list the directories to be monitored", default="list", required=True)
group.add_argument("-t", "--type", dest="type", choices=("a", "b"), help="Type of spooler job", default=None)
group.add_argument("-p", "--path", dest="path", help="Absolute path of the directory to be monitored", default=None)
group.add_argument("-r", "--release", dest="release", help="Directory path gets assigned automatically based on the release", default=None)

parser.add_argument("-c", "--codeline", dest="codeline", choices=("x","y","z"), default=None, required=True)