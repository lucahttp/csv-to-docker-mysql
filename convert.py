import pandas as pd
import sqlite3
import time
import os.path
import datetime
import string
import numpy
import wget
import sys

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


class databaseTool:
    def __init__(self):
        self.url = None
        self.file = None

        #self.directory = './'
        self.directory = '/app/'
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
        #open(filefolder, 'wb').write(myfile.content)
        print("Download finished")
        pass

    def checkExistIfYesRename(self, filefolder):
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

    def linux_fix(self):
        import os

        def opensed(text):
            content = os.popen(text).read()
            pass

        #opensed("sed -n '/14:00/, +3p' mon")
        opensed("""sed -i '/CREATE TABLE /,\@);@ s/"//' ./myquery.sql""")
        opensed("""sed -i '/CREATE TABLE /,\@);@ s/"//' ./myquery.sql""")
        opensed("""sed -i '/CREATE TABLE /,\@);@ s/INTEGER/int/' ./myquery.sql""")
        opensed("""sed -i '/CREATE TABLE /,\@);@ s/REAL/float/' ./myquery.sql""")
        opensed("""sed -i '/CREATE TABLE /,\@);@ s/TEXT/VARCHAR(255)/' ./myquery.sql""")

        pass

    def createDataFrame(self, csvpath):

        self.dataframe = pd.read_csv(csvpath)
        return self.dataframe

    def createMySQLDB(self, frame):
        # Import module
        import pymysql
        # create connection
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='')
        # Create cursor
        my_cursor = connection.cursor()
        # Execute Query
        #my_cursor.execute("DROP DATABASE IF EXISTS mydatabase;CREATE DATABASE mydatabase;USE mydatabase;")
        my_cursor.execute("DROP DATABASE IF EXISTS mydatabase;")
        my_cursor.execute("CREATE DATABASE mydatabase;")
        my_cursor.execute("USE mydatabase;")
        #my_cursor.execute("SELECT * from *")
        my_cursor.execute("SHOW DATABASES;")
        # Fetch the records
        result = my_cursor.fetchall()
        for i in result:
            print(i)
        # Close the connection
        connection.close()
        pass

    def createMySQL_onlyDB(self):
        import pymysql
        user = 'root'
        passw = 'root' # In previous posts variable "pass"
        host =  '127.0.0.1'
        port = 3306

        database = 'mydatabase' # In previous posts similar to "schema"

        conn = pymysql.connect(host=host,
                            port=port,
                            user=user, 
                            passwd=passw)

        my_cursor = conn.cursor()
        my_cursor.execute("DROP DATABASE IF EXISTS mydatabase;")
        my_cursor.execute("CREATE DATABASE mydatabase;")
        my_cursor.execute("USE mydatabase;")
        #my_cursor.execute("SELECT * from *")
        my_cursor.execute("SHOW DATABASES;")
        # , flavor = 'mysql'
        #self.dataframe.to_sql(name=database, con=conn, if_exists = 'append', index=False)
        pass

    def createMySQL_loadtoDB(self):
        import pandas as pd
        import pymysql
        from sqlalchemy import create_engine

        user = 'root'
        passw = 'root'
        host =  '127.0.0.1'  # either localhost or ip e.g. '172.17.0.2' or hostname address 
        port = 3306 
        database = 'mydatabase'

        mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=False)

        #directory = r'directoryLocation'  # path of csv file
        csvFileName = self.csvfilepath

        df = pd.read_csv(self.csvfilepath)
    
        df.to_sql(name=csvFileName[:-4], con=mydb, if_exists = 'replace', index=False)

        """
        if_exists: {'fail', 'replace', 'append'}, default 'fail'
            fail: If table exists, do nothing.
            replace: If table exists, drop it, recreate it, and insert data.
            append: If table exists, insert data. Create if does not exist.
        """
        pass

    def createSQLiteDB(self, csvpath, dbpath):
        # read the CSV
        #df = pd.read_csv('./data/casoscovid19.csv')
        df = pd.read_csv(csvpath)
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
        df.to_sql("mydb", self.conn)
        pass

    def sqldump2(self, adatabase, aqueryfile):
        # Convert file existing_db.db to SQL dump file dump.sql
        #import sqlite3
        # sqlite3 storage.sqlite .dump > output_before.sql
        # con.close()
        pass

    def sqldump(self, adatabase, aqueryfile):
        # Convert file existing_db.db to SQL dump file dump.sql
        #import sqlite3
        con = sqlite3.connect(adatabase)
        with open(aqueryfile, 'w') as f:
            for line in con.iterdump():
                f.write('%s\n' % line)
        # con.close()
        pass

    def fixSqlQuery(self, aqueryfile):
        # Convert file existing_db.db to SQL dump file dump.sql
        #import sqlite3
        #file = "c:/Users/Luca/Documents/GitHub/csv-to-docker-mysql/data/myquery.1.sql"
        file = aqueryfile
        with open(file) as f:
            lines = f.readlines()
        # lines # ['This is the first line.\n', 'This is the second line.\n']
        lines[0] = "DROP DATABASE IF EXISTS mydatabase;\nCREATE DATABASE mydatabase;\nUSE mydatabase;\n"
        # lines # ["This is the line that's replaced.\n", 'This is the second line.\n']

        #command = "c:/xampp/mysql/bin/mysql.exe --user=root --password=''  -e 'show databases;'"
        # system(command)
        # https://www.cyberciti.biz/faq/mysql-command-to-show-list-of-databases-on-server/
        # .\mysql.exe -u root -p '' -e 'show databases;'
        # .\mysql.exe -u your-user-name -p'Your-password'
        # .\mysql.exe --user=root --password=""  -e 'show databases;'
        # C:\xampp\mysql\bin\mysql.exe --user=root --password=""  -e 'show databases;'
        # C:\xampp\mysql\bin\mysql.exe --user=root --password=""  -e "DROP DATABASE IF EXISTS mydatabase;CREATE DATABASE mydatabase;USE mydatabase;"
        # C:\xampp\mysql\bin\mysql.exe --user=root --password=""  mydatabase < myquery.sql
        # C:\xampp\mysql\bin\mysql.exe --user=root --password=""  -e "USE mydatabase;source myquery.sql;"
        # mysql> use db_name; mysql> source backup-file.sql;
        # C:\xampp\mysql\bin\mysqlimport.exe --ignore-lines=1 --lines-terminated-by='\n' --fields-terminated-by=',' --fields-enclosed-by='"' --verbose --local -uroot -proot mydatabase mydata.csv
        # C:\xampp\mysql\bin\mysqlimport.exe -uroot --columns='head -n 1 mydata.csv' --ignore-lines=1 mydatabase mydata.csv

        # C:\xampp\mysql\bin\mysqlimport.exe -h localhost -u root -p --ignore-lines=1 --fields-terminated-by=, mydatabase mydata.csv
        # C:\xampp\mysql\bin\mysqlimport.exe  --fields-terminated-by=, --verbose --local -u root -p mydatabase mydata.csv
        # INTEGER
        # TEXT
        # FLOAT
        """
        with open("/etc/apt/sources.list", "r") as sources:
            lines = sources.readlines()
        with open("/etc/apt/sources.list", "w") as sources:
            for line in lines:
                sources.write(re.sub(r'^# deb', 'deb', line))
            
        """
        with open(file, "w") as f:
            f.writelines(lines)
        pass

    def doURL(self, myurl):
        self.download(myurl, self.csvfilepath)
        #self.createSQLiteDB(self.csvfilepath, self.dbfilepath)
        #self.sqldump(self.dbfilepath, self.queryfilepath)
        # self.fixSqlQuery(self.queryfilepath)
        self.createDataFrame(self.csvfilepath)
        self.createMySQL_onlyDB()
        self.createMySQL_loadtoDB()
        pass

    def doFILE(self, myfile):
        # self.download(self.url, self.csvfilepath)
        self.createSQLiteDB(myfile, self.dbfilepath)
        self.sqldump(self.dbfilepath, self.queryfilepath)
        self.fixSqlQuery(self.queryfilepath)
        pass

#url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
#mytool = databaseTool(url)
# mytool.do()


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
    mytool = databaseTool()
    mytool.doURL(url)
elif "-p" in opts:
    #print(" ".join(arg.lower() for arg in args))
    file = args[0]
    mytool = databaseTool()
    mytool.doFILE(file)
else:
    raise SystemExit(
        f"Usage: {sys.argv[0]} (-u for an URL | -p for a path to csv file ) <arguments>...")



