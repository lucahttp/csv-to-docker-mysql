FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root

#ADD scripts /csv2sql/

#RUN for file in /csv2sql/* do cat "$file" >> results.out done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done


#RUN python3 /app/convert.py -u 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
#RUN python3 /app/convert.py -u ${URL}

#RUN echo    "cd /app/ \n" \ 

#		"python3 /app/convert.py -u https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv \n" \ 
#		"echo 'Congratulations'" > /app/convert_task.sh
#RUN chmod 777 /app/convert_task.sh
#RUN cp /app/convert_task.sh /docker-entrypoint-initdb.d/
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



# awk 'NR==1{sub("AccountSettings","Users")};1' input.txt  
#RUN cp /app/myquery.sql /docker-entrypoint-initdb.d/
# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory

# https://stackoverflow.com/questions/26504846/copy-directory-to-other-directory-at-docker-using-add-command


#RUN for i in *.csv; do echo "hello $i"; done

#RUN for i in *.csv; do /csv2sql/convert.sh -f $i ; done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done

#RUN /csv2sql/convert.sh /csv2sql/my.csv

#RUN sed '1iCREATE DATABASE DatabaseName;' my.sql
#RUN sed '2iUSE DatabaseName;' my.sql

#RUN for i in *.sql; do cp $i /docker-entrypoint-initdb.d/ ; done


#https://unix.stackexchange.com/questions/438105/remove-certain-characters-in-a-text-file
#sed -e 's/.*]//' -e 's/  */ /g' file.txt

#RUN cp /csv2sql/my.sql /docker-entrypoint-initdb.d/

#RUN echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION" > /my2.sql

# https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
# https://github.com/docker-library/mysql/issues/129
RUN echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" > /0createuser_fix.sql
RUN echo "mysqld --general-log=1 --general-log-file=/general-log.log" > /0setlogs_fix.sh
RUN echo "mysqld --max-allowed-packet=67108864" > /1setlogs_fix.sh

#RUN echo "set global max_allowed_packet=67108864;" > /fix_1.sql

RUN cp /*_fix.sql /docker-entrypoint-initdb.d/
RUN cp /*_fix.sh /docker-entrypoint-initdb.d/

#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

#RUN mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='ID,Name,Phone,Address' --local -u root -p Database /path/to/csvfile/TableName.csv
EXPOSE 3306


#CMD ["convert.py -u https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]
#CMD ["server.py"]
#CMD ["server.py -u https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]


#ENTRYPOINT ["python3"]
#CMD ["server.py", "-u", "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]

#ENTRYPOINT ["/bin/bash", "-c", "cat"]
#CMD ["/app/server.py -u https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/casos-covid-19/casos_covid19.csv"]

#VOLUME [ "/app" ]