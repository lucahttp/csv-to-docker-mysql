FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root

ARG URL="https://people.sc.fsu.edu/~jburkardt/data/csv/grades.csv" 
#ENV DATASOURCEFILE="mycsvfile.csv"


RUN apt update -y
RUN apt install wget -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install sqlite3 -y
#COPY scripts/convert2.sh /convert.sh
#COPY scripts/my.csv /my.csv
RUN  mkdir  /app/
WORKDIR /app/

COPY convert.py /app/convert.py
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
#COPY scripts/ /csv2sql/
#RUN wget https://raw.githubusercontent.com/lukaneco/CSV-to-MySql/master/convert.sh -O /csv2sql/convert.sh
#RUN wget https://github.com/lukaneco/CSV-to-MySql/blob/master/convert.sh -O /csv2sql/convert.sh
RUN chmod 777 /app/convert.py

#RUN wget https://people.sc.fsu.edu/~jburkardt/data/csv/grades.csv -O /app/${DATASOURCEFILE}
#ADD data /csv2sql/
#./convert.sh -f example/mycsvfile.csv
RUN ls /app/
#ADD scripts /csv2sql/

#RUN for file in /csv2sql/* do cat "$file" >> results.out done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done


#RUN python3 /app/convert.py -u 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
#RUN python3 /app/convert.py -u ${URL}

RUN echo    "cd /app/ \n" \ 
		"python3 /app/convert.py -u https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv \n" \ 
		"echo 'Congratulations'" > /app/convert_task.sh
RUN chmod 777 /app/convert_task.sh
RUN cp /app/convert_task.sh /docker-entrypoint-initdb.d/
#RUN echo "cd /app/ \n python3  /app/convert.py -u https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv \n echo 'Congratulations'" > /app/convert_task.sh

#RUN sed -i "1iUSE $DATABASE;" /app/myquery.sql
#RUN sed '1 s/^.*\$/DROP DATABASE IF EXISTS ${DATABASE};\nCREATE DATABASE ${DATABASE};\nUSE ${DATABASE};/' /app/myquery.sql
#sed '1cDROP DATABASE IF EXISTS mydatabase;\nCREATE DATABASE mydatabase;\nUSE mydatabase;\n' myquery.1.sql


#var="DROP DATABASE IF EXISTS mydatabase;\nCREATE DATABASE mydatabase;\nUSE mydatabase;\n"
#sed -i "1s/.*/$var/" myquery.1.sql
#RUN sed -i '/CREATE TABLE mydb (/,\@);@ s/"//' ./test.1.sql

#RUN sed -i '/CREATE TABLE /,\@);@ s/"//' ./myquery.sql
#RUN sed -i '/CREATE TABLE /,\@);@ s/"//' ./myquery.sql

#RUN sed -i '/CREATE TABLE /,\@);@ s/INTEGER/int/' ./myquery.sql
#RUN sed -i '/CREATE TABLE /,\@);@ s/REAL/float/' ./myquery.sql
#RUN sed -i '/CREATE TABLE /,\@);@ s/TEXT/VARCHAR(255)/' ./myquery.sql

RUN cat



# awk 'NR==1{sub("AccountSettings","Users")};1' input.txt  
#RUN cp /app/myquery.sql /docker-entrypoint-initdb.d/
# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory

# https://stackoverflow.com/questions/26504846/copy-directory-to-other-directory-at-docker-using-add-command


#RUN for i in *.csv; do echo "hello $i"; done

#RUN for i in *.csv; do /csv2sql/convert.sh -f $i ; done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done

#RUN /csv2sql/convert.sh /csv2sql/my.csv
RUN ls /app/

#RUN sed '1iCREATE DATABASE DatabaseName;' my.sql
#RUN sed '2iUSE DatabaseName;' my.sql

#RUN for i in *.sql; do cp $i /docker-entrypoint-initdb.d/ ; done


#https://unix.stackexchange.com/questions/438105/remove-certain-characters-in-a-text-file
#sed -e 's/.*]//' -e 's/  */ /g' file.txt

#RUN cp /csv2sql/my.sql /docker-entrypoint-initdb.d/

#RUN echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION" > /my2.sql

# https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
# https://github.com/docker-library/mysql/issues/129
RUN echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" > /app/0createuser.sql

RUN cp /app/0createuser.sql /docker-entrypoint-initdb.d/

#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

#RUN mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='ID,Name,Phone,Address' --local -u root -p Database /path/to/csvfile/TableName.csv

EXPOSE 3306