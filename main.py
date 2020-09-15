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

SQLALCHEMY_POOL_RECYCLE=90

run=None
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
        self.MySQL_passw = 'root' # In previous posts variable "pass"
        self.MySQL_host =  '127.0.0.1'
        self.MySQL_port = 3306

        self.MySQL_database = 'mydatabase' # In previous posts similar to "schema"

        self.dbtype = "SQLITE"
        


    def setDBType(self,dbtype):
        self.dbtype = dbtype
        pass
    def loadUserMySQL(self, someuser, somepass, somehost,someport,somedatabase):
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
        self.MySQL_host =  somehost
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
    

        # https://www.geeksforgeeks.org/python-test-if-string-contains-element-from-list/
        test_list = ['.zip', '.7zip'] 
        
        if any(ele in url for ele in test_list):
            tmpSTAMP =  "tmp"
            tmpfile =  "tmp" + filefolder
            wget.download(url, tmpfile, bar=bar_custom)     
            #x.replace('.good','')
            pass
        else:
            wget.download(url, filefolder, bar=bar_custom)
            pass
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
        filename = url[url.rfind("/")+1:]

        basename = os.path.basename(filename)
        onlyname = os.path.splitext(basename)
        newfilename = onlyname[0] + self.getTime() + onlyname[1]
        if onlyname[1] == ".zip":

            pass
        else:
            pass
        self.csvfilepath = self.directory + onlyname[0] + ".csv"
        print(self.csvfilepath)
        self.dbfilepath = self.directory + onlyname[0] + ".db"
        print(self.dbfilepath) 
        self.mytable = onlyname[0]
        print(self.mytable)
        pass

    def setFILE(self,filePath):
        self.whatis = "FILE"
        self.file = filePath
        self.csvfilepath = filePath

        basename = os.path.basename(filePath)
        onlyname = os.path.splitext(basename)
        #newfilename = onlyname[0] + self.getTime() + onlyname[1]
        if onlyname[1] == ".zip":

            pass
        else:
            pass
        #self.csvfilepath = self.directory + onlyname[0] + ".csv"
        print(self.csvfilepath)
        self.dbfilepath = self.directory + onlyname[0] + ".db"
        print(self.dbfilepath) 
        self.mytable = onlyname[0]
        print(self.mytable)
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
                    self.download(self.url,self.csvfilepath)
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
            self.download(self.url,self.csvfilepath)
            self.flag_downloading = False
            self.databaseIsUpdated = False
            print("Downloading Finished")
            pass
        pass


    def updateDataframe(self):
        print(self.csvfilepath)
        self.dataframe = pd.read_csv(self.csvfilepath)
        pass

    def createTable(self):
        import mysql.connector
        MYSQL_USER=self.MySQL_user
        MYSQL_PASSWORD=self.MySQL_passw
        MYSQL_HOST=self.MySQL_host
        MYSQL_DATABASE=self.MySQL_database
        MYSQL_PORT=self.MySQL_port 

        CONNECT = mysql.connector.connect(port=MYSQL_PORT,user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, database=MYSQL_DATABASE, charset='utf8' , buffered=True, connection_timeout=300)
        CURSOR = CONNECT.cursor(buffered=True)
        #query="SHOW DATABASES;"
        #CURSOR.execute(query)
        database= self.MySQL_database
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
        host =  self.MySQL_host
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
        host =  self.MySQL_host
        port = self.MySQL_port 
        database = self.MySQL_database

        mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)

        #directory = r'directoryLocation'  # path of csv file

    
        self.dataframe.to_sql(name=(self.csvfilepath)[:-4], con=mydb, if_exists = 'replace', index=False)
        pass


    def makeReport(self,query_name,query):
        # https://stackoverflow.com/questions/4899832/sqlite-function-to-format-numbers-with-leading-zeroes
        # https://tiebing.blogspot.com/2011/07/sqlite-3-string-to-integer-conversion.html
        """
        CAST(substr('00'||residencia_provincia_id,-2) || substr('000'||residencia_departamento_id,-3) as integer) AS ID,
        """
        sql_string = """
        SELECT residencia_departamento_nombre  AS "Departamento Residencia",residencia_provincia_nombre  AS "Provincia Residencia", 
        substr('00'||residencia_provincia_id,-2) || substr('000'||residencia_departamento_id,-3) AS ID,
        substr('000'||residencia_departamento_id,-3) AS "ID Departamento",
        substr('00'||residencia_provincia_id,-2) AS "ID Provincia",
        count(*) AS "Total Test",
        sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end) AS Confirmados,
        sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end) AS Recuperados,
        (sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end)-sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end))Activos,
        sum(case when clasificacion = "Caso confirmado - Fallecido" then 1 else 0 end) AS Fallecidos
        FROM mydb
        GROUP BY residencia_departamento_nombre
        ORDER BY "residencia_provincia_id" ASC,"residencia_departamento_nombre" ASC,"residencia_departamento_nombre" ASC;
        """
        sql_string = query
        gg = pd.read_sql(sql_string, self.conn)
        print()
        #return self.makeReport(gg, "fullreport")
        gg = gg
        report_name = "fullreport"
        report_name = query_name
        #def makeReport(self, gg, report_name):
        import json
        # print(type(gg))
        #gg = gg.set_index(0)
        print(type(gg))
        gg.to_csv(report_name+".csv", encoding='latin1', index=False)
        file = report_name+".csv"
        # https://pandas.pydata.org/pandas-docs/dev/reference/api/pandas.DataFrame.to_json.html
        alternative = gg.to_json(orient="records")

        alternative_parsed = json.loads(alternative)

        alternative_parsed_gg = json.dumps(alternative_parsed, indent=4)  
        # https://stackoverflow.com/questions/46831294/convert-each-row-of-pandas-dataframe-to-a-separate-json-string
        """
        for chunk in pd.read_csv(file, sep = ",", header = False, index_col = 0):
            json_chunk = chunk.to_json(orient = "records", force_ascii = True, default_handler = None)
        """
        #json.dumps(parsed, indent=4, ensure_ascii=False)
        # gg.set_index(list(gg)[0])
        gg = gg.set_index(gg.columns[0])
        gg.set_index(gg.columns.tolist()[0])
        #json.dumps(parsed, indent=4)

        result = gg.to_json(orient="index")
        parsed = json.loads(result)
        resultado = gg.to_json(orient="index")
        gg.to_json(report_name+".json", orient='table',
                   force_ascii=False, indent=4)

        # Works
        #out = json.dumps(parsed, indent=4, ensure_ascii=False)
        #gg.to_csv('report.csv', encoding='utf-8', index=False)

        #result = gg.to_json(orient="index")

        parsed = json.loads(result)

        json.dumps(parsed, indent=4)

        # print(resultado)
        return alternative_parsed_gg
        
    def createDB(self, csvpath, dbpath):
        # read the CSV
        #df = pd.read_csv('./data/casoscovid19.csv')
        #df = pd.read_csv(csvpath)
        # connect to a database
        #conn = sqlite3.connect("casoscovid19.db")
        self.conn = sqlite3.connect(dbpath)
        # if the db does not exist, this creates a Any_Database_Name.db file in the current directory
        # store your table in the database:

        cursor = self.conn.cursor()
        # Doping EMPLOYEE table if already exists
        cursor.execute("DROP TABLE IF EXISTS mydb;")
        #print("Table dropped... ")
        # Commit your changes in the database
        self.conn.commit()
        # Closing the connection
        # conn.close()
        # https://www.tutorialspoint.com/python_sqlite/python_sqlite_drop_table.htm

        #gg = pd.read_sql('DROP TABLE IF EXISTS test_0;', conn)
        #pd.read_sql_query('DROP TABLE IF EXISTS test_0;', conn)
        self.dataframe.to_sql("mydb", self.conn)
        pass

    def localip(self):
        import socket 
        print(self.MySQL_host)
        try: 
            host_name = socket.gethostname() 
            host_ip = socket.gethostbyname(host_name) 
            print("Hostname :  ",host_name) 
            print("IP : ",host_ip) 
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
        print("The FIle is",self.csvfilepath)
        # self.download(self.url, self.csvfilepath)
        #self.createSQLiteDB(self.file, self.dbfilepath)
        #self.sqldump(self.dbfilepath, self.queryfilepath)
        #self.fixSqlQuery(self.queryfilepath)
        pass

    def run(self):
        if self.whatis == "URL":
            print("Setting url source")
            self.updateCheckURL()
            print("updating Dataframe")
            self.updateDataframe()
            print("updating Database")
            
            self.firstRun()
            if self.databaseIsUpdated == False:
                print("The Database is not updated")

                if self.dbtype == "MSYQL":
                    self.createTable()
                    self.updateDB()
                    pass
                if self.dbtype == "SQLITE":
                    self.delete(self.dbfilepath)
                    self.createDB(self.csvfilepath, self.dbfilepath)
                    print(self.dbfilepath)
                    self.conn = sqlite3.connect(self.dbfilepath)
                    pass
                else:
                    self.delete(self.dbfilepath)
                    self.createDB(self.csvfilepath, self.dbfilepath)
                    print(self.dbfilepath)
                    self.conn = sqlite3.connect(self.dbfilepath)
                    pass
                
                self.databaseIsUpdated == True
                pass
            else:
                print("The Database is updated")

                pass
            
            pass
        elif self.whatis == "FILE":
            print("Setting file source")
            self.updateCheckFILE()
            print("updating Dataframe")
            self.updateDataframe()
            print("updating Database")
            
            self.firstRun()
            if self.databaseIsUpdated == False:
                print("The Database is not updated")

                if self.dbtype == "MSYQL":
                    self.createTable()
                    self.updateDB()
                    pass
                if self.dbtype == "SQLITE":
                    self.delete(self.dbfilepath)
                    self.createDB(self.csvfilepath, self.dbfilepath)
                    print(self.dbfilepath)
                    self.conn = sqlite3.connect(self.dbfilepath)
                    pass
                else:
                    self.delete(self.dbfilepath)
                    self.createDB(self.csvfilepath, self.dbfilepath)
                    print(self.dbfilepath)
                    self.conn = sqlite3.connect(self.dbfilepath)
                    pass
                
                self.databaseIsUpdated == True
                pass
            else:
                print("The Database is updated")

                pass
            self.updateCheckFILE()
            pass
        else:
            print("Nothing selected")
            pass
        #run=False
        pass


#url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
#mytool = databaseTool(url)
# mytool.do()
mytool = databaseTool()

"""
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
"""
##############################################################################################################
# GUI
##############################################################################################################
import argparse
# https://pymotw.com/2/argparse/
parser = argparse.ArgumentParser()

parser.add_argument('-u', action='store', dest='url_value',
                    help='here you can specify the url to the csv')

parser.add_argument('-p', action='store', dest='path_value',
                    help='here you can specify the PATH to the csv')

parser.add_argument('-t', action='store', dest='type_value',
                    help='here you can specify the type of database like SQLITE, MYSQL')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')


results = parser.parse_args()
print('URL              =', results.url_value)
#url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
myurl = results.url_value
mypath = results.path_value
if myurl == None:
    print(type(myurl))
    myurl = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"



    if mypath == None:
        print ("Input not exist")
        pass
    else:
        import pathlib
        #file = pathlib.Path("guru99.txt")
        file = pathlib.Path(mypath)
        if file.exists ():
            print ("File exist")
            run=True
            mytool.setFILE(mypath)

        else:
            print ("File not exist")
        pass
    pass
else:
    run=True
    mytool.setURL(myurl)
    pass

if myurl == None:
    print(type(myurl))
    myurl = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
    pass
else:
    pass

mytool.setURL(myurl)

print('DB TYPE          =', results.type_value)
#url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
mydbtype = results.type_value
if mydbtype == None:
    print(type(mydbtype))
    mydbtype = "SQLITE"
    pass
else:
    mytool.setDBType(mydbtype)
    pass

    pass

mytool.setDBType(mydbtype)


##############################################################################################################
# GUI
##############################################################################################################


beat.set_rate(1/(60*60*8))  # 2 Hz
try:
    if run==True:
        while beat.true():
            # do some time consuming work here
            #mytool.loadUserMySQL("DCMTLY0kMT","3hDcVT6IdQ","remotemysql.com",3306,"DCMTLY0kMT")
            mytool.loadUserMySQL("admin","admin","127.0.0.1",3306,"mydatabase")
            mytool.localip()
            mytool.run()
            print("Now the system is up to date")
            beat.sleep()  # total loop duration would be 0.5 sec
            pass
        pass
    else:
        print("🧙 Bye")
        exit()
        pass
except KeyboardInterrupt:
    print("🧙 Bye")
    exit()
    pass
    while beat.true():
        # do some time consuming work here
        #mytool.loadUserMySQL("DCMTLY0kMT","3hDcVT6IdQ","remotemysql.com",3306,"DCMTLY0kMT")
        mytool.loadUserMySQL("admin","admin","127.0.0.1",3306,"mydatabase")
        mytool.localip()
        mytool.run()
        print("Now the system is up to date")
        beat.sleep()  # total loop duration would be 0.5 sec
    pass
except KeyboardInterrupt:
    print("🧙 Bye")
    exit()
    pass
"""
myurl = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
mytool.setURL(myurl)
mytool.run()

sql_string = """
        SELECT residencia_departamento_nombre  AS "Departamento Residencia",residencia_provincia_nombre  AS "Provincia Residencia", 
        substr('00'||residencia_provincia_id,-2) || substr('000'||residencia_departamento_id,-3) AS ID,
        substr('000'||residencia_departamento_id,-3) AS "ID Departamento",
        substr('00'||residencia_provincia_id,-2) AS "ID Provincia",
        count(*) AS "Total Test",
        sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end) AS Confirmados,
        sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end) AS Recuperados,
        (sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end)-sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end))Activos,
        sum(case when clasificacion = "Caso confirmado - Fallecido" then 1 else 0 end) AS Fallecidos
        FROM mydb
        GROUP BY residencia_departamento_nombre
        ORDER BY "residencia_provincia_id" ASC,"residencia_departamento_nombre" ASC,"residencia_departamento_nombre" ASC;
        """
asdfgbawesbrj = mytool.makeReport("test",sql_string)


sql_asdqwedascawe = """
SELECT fecha_apertura  AS "Fecha",
	 count(*) AS "Cantidad de test",
    sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end) AS Confirmados,
    sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end) AS Recuperados,
    (sum(case when clasificacion_resumen="Confirmado" then 1 else 0 end)-sum(case when clasificacion LIKE "%No Activo%" then 1 else 0 end))Activos,
    sum(case when clasificacion = "Caso confirmado - Fallecido" then 1 else 0 end) AS Fallecidos
FROM mydb
GROUP BY fecha_apertura
ORDER BY "fecha_apertura" DESC;
"""
asfwetsdgerygert = mytool.makeReport("asdqwe",sql_asdqwedascawe)
##############################################################################################################
# Web Server
##############################################################################################################

# https://medium.com/@kshitijvijay271199/flask-on-google-colab-f6525986797b
from flask_ngrok import run_with_ngrok
from flask import Flask
import json
app = Flask(__name__)
#run_with_ngrok(app)   #starts ngrok when the app is run@app.route("/")

@app.route("/a")
def asdwd():
    #return "<h1>Running Flask on Google Colab!</h1>"
    #data = table.to_json(orient="index", force_ascii=False, indent=4)
    data = asfwetsdgerygert
    response = app.response_class(
        response=data,
        # response=data,
        status=200,
        mimetype='application/json'
        # text/plain, text/html, text/css, text/javascript application/json
        # https://developer.mozilla.org/es/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    )
    #https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route("/")
def home():
    #return "<h1>Running Flask on Google Colab!</h1>"
    #data = table.to_json(orient="index", force_ascii=False, indent=4)
    data = asdfgbawesbrj
    response = app.response_class(
        response=data,
        # response=data,
        status=200,
        mimetype='application/json'
        # text/plain, text/html, text/css, text/javascript application/json
        # https://developer.mozilla.org/es/docs/Web/HTTP/Basics_of_HTTP/MIME_types
    )
    return response



#app.run(port=5000, debug=True, use_reloader=True)
app.run()
# docker-compose up --force-recreate --renew-anon-volumes --build
#app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=True)
