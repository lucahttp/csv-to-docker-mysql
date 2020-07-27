fname="$1"
sed 's/\s*,*\s*$//g' "$fname" > tmp.csv
op=$(echo "$fname" | cut -d"." -f 1)
TABLE=$op"-table"
DATABASE=$op
opfile="$op.sql"
op="\`$op\`"
columns=$(head --lines=1 tmp.csv | sed 's/,/`,`/g' | tr -d "\r\n")


columns="\`$columns\`"
tail --lines=+2 tmp.csv | while read l ; do
values=$(echo $l | sed 's/,/\",\"/g' | tr -d "\r\n")
values="\"$values\""
echo "INSERT INTO $op($columns) VALUES ($values);"
done > "$opfile"



#CREATE TABLE Persons(PersonID int,LastName varchar(255));
#$tablecolumnstypes="\`$tablecolumnstypes\`"
#echo $tablecolumnstypes
#https://stackoverflow.com/questions/9998596/create-mysql-table-directly-from-csv-file-using-the-csv-storage-engine
#http://positon.org/import-csv-file-to-mysql


DELIM=","

#CSV="$1"
CSV="tmp.csv"


FIELDS=$(head -1 "$CSV" | sed -e 's/'$DELIM'/` varchar(255),\n`/g' -e 's/\r//g')
echo $FIELDS
FIELDS='`'"$FIELDS"'` varchar(255)'

echo $FIELDS

sed "1iCREATE DATABASE '$DATABASE';\nUSE '$DATABASE';" $opfile

#sed "1iCREATE DATABASE '$DATABASE';\nUSE '$DATABASE';" $opfile
sed "3iDROP TABLE IF EXISTS '$TABLE';\nCREATE TABLE '$TABLE' ($FIELDS)" $opfile
#\nCREATE TABLE '$TABLE' ('$FIELDS');
echo "DROP TABLE IF EXISTS '$TABLE';\nCREATE TABLE '$TABLE' ($FIELDS)"
#echo "DROP TABLE IF EXISTS '$TABLE';"
#echo $FIELDS
#echo "CREATE TABLE '$TABLE' ($FIELDS);"

rm tmp.csv