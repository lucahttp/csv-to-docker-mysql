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