from argparse import ArgumentParser

parser = ArgumentParser(description="Tool to keep archiving tar files")
sub = parser.add_subparsers(dest='action')
sp1 = sub.add_parser('start')
sp2 = sub.add_parser('stop')
sp3 = sub.add_parser('list')
#parser.add_argument("-a", "--action", dest="action", choices=("start", "stop", "list"), help="start/stop/list the directories to be monitored", default="list", required=True)
for sp in [sp1,sp2]:
    sp.add_argument("-t", "--type", dest="type", choices=("a", "b"), help="Type of spooler job", default=None)
    sp.add_argument("-p", "--path", dest="path", help="Absolute path of the directory to be monitored", default=None)
    sp.add_argument("-c", "--codeline", dest="codeline", choices=("x","y","z"), default=None, required=True)
    sp.add_argument("-r", "--release", dest="release", help="Directory path gets assigned automatically based on the release", default=None)

for astr in [
    'list',
    'start -t a -p /tmp -c x',
    'start -t b -r rr -c y',
    'start']:
    print(parser.parse_args(astr.split()))