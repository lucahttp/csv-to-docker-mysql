import argparse
import sys
import wget
import numpy
import string
import os.path
import sqlite3
import pandas as pd
import cronus.beat as beat
import time
import datetime

SQLALCHEMY_POOL_RECYCLE = 90


def getTime():
    x = datetime.datetime.now()
    xs = x.strftime("%X %x")
    datestring = str(xs)
    datestring = datestring.replace(":", "-")
    datestring = datestring.replace("/", "-")
    datestring = datestring.replace(" ", "--")
    # print(datestring)
    return datestring


def do_some_work():
    # time.sleep(0.3)
    print("Doing stuff..."+getTime())


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


class databaseTool:
    def __init__(self):
        self.url = None
        self.file = None
        self.whatis = None
        self.tableexist = None

        #self.directory = './'
        self.directory = './'
        # Files
        self.csvfilepath = self.directory + 'mydata.csv'
        self.dbfilepath = self.directory + 'mydb.db'
        self.mytable = 'mydb'
        self.queryfilepath = self.directory + 'myquery.sql'
        #self.csvfilereport = "report.csv"
        # SQLite
        self.conn = None
        self.dataframe = None
        # Data
        #self.countAllCases = None
        # Flags
        self.flag_downloading = False
        self.flag_download_current = 0
        self.flag_download_total = 0
        self.flag_download_percent = 0

        self.flag_creating = False

        self.persistent = False
        self.firstrun = True

        self.databaseIsUpdated = None
        # DB
        self.MySQL_user = 'root'
        self.MySQL_passw = 'root'  # In previous posts variable "pass"
        self.MySQL_host = '127.0.0.1'
        self.MySQL_port = 3306

        self.MySQL_database = 'mydatabase'  # In previous posts similar to "schema"
        
        self.dbtype = "SQLITE" # MYSQL

    def loadUserMySQL(self, someuser, somepass, somehost, someport, somedatabase):
        """Function To load user info to connect to an MySQL DB
        Example:

        someuser = 'root'
        somepass = 'root'
        somehost = '127.0.0.1'
        someport = 3306
        somedatabase = 'mydatabase'
        """

        self.MySQL_user = someuser
        self.MySQL_passw = somepass
        self.MySQL_host = somehost
        self.MySQL_port = someport
        self.MySQL_database = somedatabase
        pass

    def download(self, url, filefolder):
        print("Download started")
        #myfile = requests.get(url, allow_redirects=True)

        def bar_custom(current, total, width=80):
            self.flag_download_current = current
            self.flag_download_total = total
            self.flag_download_percent = current / total * 100
            print("Downloading: %d%% [%d / %d] bytes" %
                  (current / total * 100, current, total))
        #wget.download(url, bar=bar_custom)
        wget.download(url, filefolder, bar=bar_custom)
        #wget.download(url, filefolder)
        #open(filefolder, 'wb').write(myfile.content)
        print("Download finished")
        pass

    def checkExistIfYesRename(self, filefolder):
        print("Going to check")
        import os.path

        if os.path.exists(filefolder):
            # get the path to the file in the current directory
            #src = os.path.realpath(filefolder)
            # rename the original file
            basename = os.path.basename(filefolder)
            onlyname = os.path.splitext(basename)
            newfilename = onlyname[0] + self.getTime() + onlyname[1]
            os.rename(filefolder, newfilename)
        print("Check finished")
        pass

    def setURL(self, url):
        self.whatis = "URL"
        self.url = url
        filename = url[url.rfind("/")+1:]
        self.csvfilepath = self.directory + filename
        self.dbfilepath = self.directory + filename
        self.mytable = filename
        pass

    def setFILE(self, filePath):
        self.whatis = "FILE"
        self.file = filePath
        pass

    def getTime(self):
        import datetime
        x = datetime.datetime.now()
        xs = x.strftime("%X %x")
        datestring = str(xs)
        datestring = datestring.replace(":", "-")
        datestring = datestring.replace("/", "-")
        datestring = datestring.replace(" ", "--")
        print(datestring)
        return datestring

    def getLastUpdateOfFile(self, file):

        print()
        print("file : "+file)

        created = os.path.getctime(file)
        return created

    # add time to a specific date to create the due date
    def delete(self, filetopath):
        import os
        try:
            os.remove(filetopath)
            pass
        except FileNotFoundError:
            print("Can not delete the file as it doesn't exists")
            pass
        pass

    def setPassDay(self, mydate):

        #print("incoming date " + str(mydate))

        theNextDay = mydate + datetime.timedelta(days=1)
        theNextDay = theNextDay.replace(
            hour=20, minute=00, second=00, microsecond=00)

        #print("outgoing date " + str(theNextDay))

        from tabulate import tabulate
        #print(tabulate([['2020-08-14 16:36:08','2020-08-15 20:00:00','2020-08-14 19:15:00'], []], headers=["File Date", "File Expiration Date","Current Date"]))
        print()
        print(tabulate([[str(mydate.replace(microsecond=00)), str(theNextDay), str(datetime.datetime.now(
        ).replace(microsecond=00))], []], headers=["File Date", "File Expiration Date", "Current Date"]))

        return theNextDay

    def rename(self, filefolder):
        print("Going to check")
        import os.path

        if os.path.exists(filefolder):
            # get the path to the file in the current directory
            #src = os.path.realpath(filefolder)
            # rename the original file
            basename = os.path.basename(filefolder)
            onlyname = os.path.splitext(basename)
            newfilename = onlyname[0] + self.getTime() + onlyname[1]
            os.rename(filefolder, newfilename)
        print("Check finished")
        pass

    def LeaveToTrash(self):
        if self.persistent == True:
            self.rename(self.csvfilepath)
            self.rename(self.dbfilepath)
            pass
        else:
            self.delete(self.csvfilepath)
            self.delete(self.dbfilepath)
            pass
        pass

    def CheckIfPassOneDayAfterYourCreation(self, mydate):

        # print(mydate)
        #print("the date of the file date is: " + str(datetime.datetime.fromtimestamp(mydate)))

        # from tabulate import tabulate
        # print(tabulate([['2020-08-14 16:36:08','2020-08-15 20:00:00','2020-08-14 19:15:00'], []], headers=["File Date", "File Expiration Date","Current Date"]))

        myInputDate = datetime.datetime.fromtimestamp(mydate)

        myOut = None

        if self.setPassDay(myInputDate) < datetime.datetime.now():
            #print("es mas grande")
            print("ya vencio"+" - es mas grande")
            myOut = True
            pass
        else:
            print("es mas chico")
            print("todavia no vencio"+" - es mas chico")
            myOut = False
            #print("pass the due date")
            pass

        print("vencido = "+str(myOut))

        return myOut

    def updateCheckURL(self):
        if os.path.isfile(self.csvfilepath):
            print("CSV file exist")
            # test if file pass the due date
            if self.CheckIfPassOneDayAfterYourCreation(self.getLastUpdateOfFile(self.csvfilepath)):
                print("pass the due date")

                if self.flag_downloading == True:
                    print("Is Already downloading")
                    pass
                else:
                    print("Downloading Started")
                    self.flag_downloading = True
                    self.LeaveToTrash()
                    self.download(self.url, self.csvfilepath)
                    self.flag_downloading = False
                    print("Downloading Finished")

                    self.databaseIsUpdated = False
                    pass

                pass
            else:
                print("all okay - not pass the due date")
                pass
            pass
        else:
            print("CSV file not exist")
            print("Downloading Started")
            self.flag_downloading = True
            self.LeaveToTrash()
            self.download(self.url, self.csvfilepath)
            self.flag_downloading = False
            self.databaseIsUpdated = False
            print("Downloading Finished")
            pass
        pass

    def updateDataframe(self):
        self.dataframe = pd.read_csv(self.csvfilepath)
        pass

    def createTable(self):
        import mysql.connector
        MYSQL_USER = self.MySQL_user
        MYSQL_PASSWORD = self.MySQL_passw
        MYSQL_HOST = self.MySQL_host
        MYSQL_DATABASE = self.MySQL_database
        MYSQL_PORT = self.MySQL_port

        CONNECT = mysql.connector.connect(port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                          host=MYSQL_HOST, database=MYSQL_DATABASE, charset='utf8', buffered=True, connection_timeout=300)
        CURSOR = CONNECT.cursor(buffered=True)
        #query="SHOW DATABASES;"
        # CURSOR.execute(query)
        database = self.MySQL_database
        CURSOR.execute("DROP DATABASE IF EXISTS "+database+";")
        CURSOR.execute("CREATE DATABASE "+database+";")
        CURSOR.execute("USE "+database+";")
        #my_cursor.execute("SELECT * from *")
        CURSOR.execute("SHOW DATABASES;")

        CONNECT.commit()
        pass

    def createTable_old(self):
        import pymysql

        user = self.MySQL_user
        passw = self.MySQL_passw
        host = self.MySQL_host
        port = self.MySQL_port
        database = self.MySQL_database

        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               passwd=passw)

        my_cursor = conn.cursor()
        my_cursor.execute("DROP DATABASE IF EXISTS "+database+";")
        my_cursor.execute("CREATE DATABASE "+database+";")
        my_cursor.execute("USE "+database+";")
        #my_cursor.execute("SELECT * from *")
        my_cursor.execute("SHOW DATABASES;")
        # , flavor = 'mysql'
        #self.dataframe.to_sql(name=database, con=conn, if_exists = 'append', index=False)
        pass

    def updateDB(self):
        if self.tableexist == True:
            print("Table exist")
            pass
        else:
            print("Table not exist")
            self.createTable()
            self.tableexist = True
            pass

        import pandas as pd
        import pymysql
        from sqlalchemy import create_engine

        user = self.MySQL_user
        passw = self.MySQL_passw
        host = self.MySQL_host
        port = self.MySQL_port
        database = self.MySQL_database

        mydb = create_engine('mysql+pymysql://' + user + ':' + passw +
                             '@' + host + ':' + str(port) + '/' + database, echo=False)

        # directory = r'directoryLocation'  # path of csv file

        self.dataframe.to_sql(name=(self.csvfilepath)[
                              :-4], con=mydb, if_exists='replace', index=False)
        pass

    def localip(self):
        import socket
        print(self.MySQL_host)
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print("Hostname :  ", host_name)
            print("IP : ", host_ip)
            #self.MySQL_host = host_ip
            #self.MySQL_host = 'localhost'
            #self.MySQL_host = str(host_ip)
        except:
            print("Unable to get Hostname and IP")
        # python-app    | pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '192.168.65.3' ([Errno 111] Connection refused)")
        # python-app | pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '9354925a15de' ([Errno 111] Connection refused)")
        # python-app | pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '172.17.0.3' ([Errno 111] Connection refused)")
        pass

    def firstRun(self):
        if self.firstrun == True:
            self.databaseIsUpdated = False
            pass
        pass

    def updateCheckFILE(self):
        # self.download(self.url, self.csvfilepath)
        #self.createSQLiteDB(self.file, self.dbfilepath)
        #self.sqldump(self.dbfilepath, self.queryfilepath)
        # self.fixSqlQuery(self.queryfilepath)
        pass

    def run(self):
        if self.whatis == "URL":
            self.updateCheckURL()
            print("updating Dataframe")
            self.updateDataframe()
            print("updating Database")

            self.firstRun()
            if self.databaseIsUpdated == False:
                print("The Database is not updated")
                self.createTable()
                self.updateDB()
                self.databaseIsUpdated == True
                pass
            else:
                print("The Database is updated")
                pass

            pass
        elif self.whatis == "FILE":
            self.updateCheckFILE()
            pass
        else:
            print("Nothing selected")
            pass
        pass


#url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
#mytool = databaseTool(url)
# mytool.do()
"""
mytool = databaseTool()

if "-c" in opts:
    print(" ".join(arg.capitalize() for arg in args))
    #url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
    #mytool = databaseTool(url)
    # mytool.do()
elif "-u" in opts:
    #print(" ".join(arg.upper() for arg in args))
    # print(args[0])
    #url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
    url = args[0]
    mytool.setURL(url)
elif "-p" in opts:
    #print(" ".join(arg.lower() for arg in args))
    myfile = args[0]
    mytool.setFILE(myfile)
else:
    raise SystemExit(
        f"Usage: {sys.argv[0]} (-u for an URL | -p for a path to csv file ) <arguments>...")

"""
###########################################################
# GUI
###########################################################


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


# timer task

beat.set_rate(1/(60*60*8))  # 2 Hz
try:
    while beat.true():
        # do some time consuming work here
        # mytool.loadUserMySQL("DCMTLY0kMT","3hDcVT6IdQ","remotemysql.com",3306,"DCMTLY0kMT")
        mytool.loadUserMySQL("admin", "admin", "127.0.0.1", 3306, "mydatabase")
        mytool.localip()
        mytool.run()
        print("Now the system is up to date")
        beat.sleep()  # total loop duration would be 0.5 sec
    pass
except KeyboardInterrupt:
    print("🧙 Bye")
    exit()
    pass
