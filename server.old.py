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

    def setURL(self,url):
        self.whatis = "URL"
        self.url = url
        pass

    def setFILE(self,filePath):
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
            src = os.path.realpath(filefolder)
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

    def CehckIfPassOneDayAfterYourCreation(self, mydate):

        # print(mydate)
        #print("the date of the file date is: " + str(datetime.datetime.fromtimestamp(mydate)))

        # from tabulate import tabulate
        # print(tabulate([['2020-08-14 16:36:08','2020-08-15 20:00:00','2020-08-14 19:15:00'], []], headers=["File Date", "File Expiration Date","Current Date"]))

        myInputDate = datetime.datetime.fromtimestamp(mydate)

        myOut = None

        if self.setPassDay(myInputDate) < datetime.datetime.now():
            #print("es mas grande")
            #print("ya vencio"+" - es mas grande")
            myOut = True
            pass
        else:
            #print("es mas chico")
            #print("vencido = "+str(covidargentina.CheckData()))
            #print("todavia no vencio"+" - es mas chico")
            myOut = False
            print("pass the due date")
            pass

        print("vencido = "+str(myOut))

        return myOut

    def CheckFileStatus(self):
        if os.path.isfile(self.csvfilepath):
            print("File exist")
            response =  self.CehckIfPassOneDayAfterYourCreation(self.getLastUpdateOfFile(self.csvfilepath))
            pass
        else:
            print("File not exist")
            response = False
            pass
        return response

    def updateCheckURL(self):
        if self.CheckFileStatus():
            print("""
            the CSV file not pass the due date
            all okay
            we only create the connection to the DB
            """)
            # connect to a database
            if os.path.isfile(self.dbfilepath):
                print("File exist")
                #filenamecontent = open(filenamepath)
                #dataso = filenamecontent.read()
            else:
                #dataso = {'thread_name': str(thread.name),'started': True, 'Status': 'please wait'}
                print("File not exist")
                #Create the DB
            pass
        else:
            if self.flag_downloading == True:
                print("Is Already Downloading IT")
                pass
            else:
                print("Preparing Downloading")
                self.flag_downloading = True
                self.LeaveToTrash()

                self.download(self.url,self.csvfilepath)
                # create db
                #self.conn = sqlite3.connect(self.dbfilepath)
                self.flag_downloading = False
                pass
            pass


        #self.download(self.url,self.csvfilepath)
        #self.createSQLiteDB(self.csvfilepath, self.dbfilepath)
        #self.sqldump(self.dbfilepath, self.queryfilepath)
        # self.fixSqlQuery(self.queryfilepath)
        #self.createDataFrame(self.csvfilepath)
        #self.createMySQL_onlyDB()
        #self.createMySQL_loadtoDB()
        pass

    def updateCheckFILE(self):
        # self.download(self.url, self.csvfilepath)
        #self.createSQLiteDB(self.file, self.dbfilepath)
        #self.sqldump(self.dbfilepath, self.queryfilepath)
        #self.fixSqlQuery(self.queryfilepath)
        pass

    def run(self):
        if self.whatis == "URL":
            self.updateCheckURL()
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


beat.set_rate(1/(60*60*8))  # 2 Hz
while beat.true():
    # do some time consuming work here
    mytool.run()
    print("Now the system is up to date")
    beat.sleep()  # total loop duration would be 0.5 sec
