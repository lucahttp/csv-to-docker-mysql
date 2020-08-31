FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root
#ENV URL "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"
ENV URL "https://gist.githubusercontent.com/lukaneco/2f321eb14e926b63521c5eb30cb0b11c/raw/ff413ac9d813914a2bdaf46abf58a9362efbb6f8/example.csv"
RUN apt update -y
RUN apt install wget -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install sqlite3 -y
#COPY scripts/convert2.sh /convert.sh
#COPY scripts/my.csv /my.csv
RUN  mkdir  /app/
#COPY scripts/ /csv2sql/
#RUN wget https://raw.githubusercontent.com/lukaneco/CSV-to-MySql/master/convert.sh -O /csv2sql/convert.sh

#RUN wget https://raw.githubusercontent.com/lukaneco/covid19-argentina/master/main.py -O /app/main.py

#RUN wget https://raw.githubusercontent.com/lukaneco/covid19-argentina/master/requirements.txt -O /app/requirements.txt
COPY requirements.txt /app/requirements.txt
#RUN wget https://github.com/lukaneco/CSV-to-MySql/blob/master/convert.sh -O /csv2sql/convert.sh
#RUN chmod 777 /csv2sql/convert.sh
#RUN wget https://gist.githubusercontent.com/lukaneco/367a14661e7a5fff7bcbc2745c825c7e/raw/0ba7d095e9832bf55fd078fdc7ac9341a5283798/example.sql -O /app/example.sql
#ADD data /csv2sql/
#./convert.sh -f example/mycsvfile.csv
RUN ls /app/
#ADD scripts /csv2sql/
RUN pip3 install -r /app/requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
# copy the content of the local src directory to the working directory
#RUN python main.py .
#RUN for file in /csv2sql/* do cat "$file" >> results.out done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done

# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory

# https://stackoverflow.com/questions/26504846/copy-directory-to-other-directory-at-docker-using-add-command

WORKDIR /app/
#RUN for i in *.csv; do echo "hello $i"; done

#RUN for i in *.csv; do /csv2sql/convert.sh -f $i ; done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done

#RUN /csv2sql/convert.sh /csv2sql/my.csv
#RUN ls /csv2sql/

#RUN sed '1iCREATE DATABASE DatabaseName;' my.sql
#RUN sed '2iUSE DatabaseName;' my.sql
RUN echo	"#!/bin/bash \n" \ 
		" \n" \ 
		"# Start the first process \n" \ 
		"./my_first_process -D \n" \ 
		"status=\$? \n" \ 
		"if [ \$status -ne 0 ]; then \n" \ 
		"  echo 'Failed to start my_first_process: \$status' \n" \ 
		"  exit \$status \n" \ 
		"fi \n" \ 
		" \n" \ 
		"# Start the second process \n" \ 
		"./my_second_process -D \n" \ 
		"status=\$? \n" \ 
		"if [ \$status -ne 0 ]; then \n" \ 
		"  echo 'Failed to start my_second_process: \$status' \n" \ 
		"  exit \$status \n" \ 
		"fi \n" \ 
		" \n" \ 
		"# Naive check runs checks once a minute to see if either of the processes exited. \n" \ 
		"# This illustrates part of the heavy lifting you need to do if you want to run \n" \ 
		"# more than one service in a container. The container exits with an error \n" \ 
		"# if it detects that either of the processes has exited. \n" \ 
		"# Otherwise it loops forever, waking up every 60 seconds \n" \ 
		" \n" \ 
		"while sleep 60; do \n" \ 
		"  ps aux |grep my_first_process |grep -q -v grep \n" \ 
		"  PROCESS_1_STATUS=\$? \n" \ 
		"  ps aux |grep my_second_process |grep -q -v grep \n" \ 
		"  PROCESS_2_STATUS=\$? \n" \ 
		"  # If the greps above find anything, they exit with 0 status \n" \ 
		"  # If they are not both 0, then something is wrong \n" \ 
		"  if [ \$PROCESS_1_STATUS -ne 0 -o \$PROCESS_2_STATUS -ne 0 ]; then \n" \ 
		"    echo 'One of the processes has already exited.' \n" \ 
		"    exit 1 \n" \ 
		"  fi \n" \ 
		"done" > script.sh
#RUN for i in *.sql; do cp $i /docker-entrypoint-initdb.d/ ; done


#https://unix.stackexchange.com/questions/438105/remove-certain-characters-in-a-text-file
#sed -e 's/.*]//' -e 's/  */ /g' file.txt

#RUN cp /csv2sql/my.sql /docker-entrypoint-initdb.d/

#RUN echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION" > /my2.sql

# https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
# https://github.com/docker-library/mysql/issues/129
RUN echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" > /app/my2.sql
RUN cp /app/my2.sql /docker-entrypoint-initdb.d/

#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

#RUN mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='ID,Name,Phone,Address' --local -u root -p Database /path/to/csvfile/TableName.csv

RUN wget -nd -np -P /app/ --recursive ${URL}
EXPOSE 3306
EXPOSE 5000
#CMD ["/etc/init.d/nullmailer", "start", "/usr/sbin/php5-fpm"]
COPY start.sh .
COPY server.py /app/server.py
# https://docs.docker.com/config/containers/multi-service_container/
ENTRYPOINT ["python3"]
#CMD ["server.py", "-u", "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]
CMD ["server.py", "-u", "https://gist.githubusercontent.com/lukaneco/2f321eb14e926b63521c5eb30cb0b11c/raw/ff413ac9d813914a2bdaf46abf58a9362efbb6f8/example.csv"]
#CMD ["mysqld", "server.py", "-u", "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]
#CMD ["server.py", "-u", "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]
#VOLUME [ "/app" ]