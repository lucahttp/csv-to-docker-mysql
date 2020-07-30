FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root

COPY scripts/convert2.sh /convert.sh
COPY scripts/my.csv /my.csv

RUN /convert.sh my.csv
RUN ls /

#RUN sed '1iCREATE DATABASE DatabaseName;' my.sql
#RUN sed '2iUSE DatabaseName;' my.sql

RUN cp /my.sql /docker-entrypoint-initdb.d/

#RUN echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION" > /my2.sql

# https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
# https://github.com/docker-library/mysql/issues/129
RUN echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" > /my2.sql

RUN cp /my2.sql /docker-entrypoint-initdb.d/

#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

#RUN mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='ID,Name,Phone,Address' --local -u root -p Database /path/to/csvfile/TableName.csv

EXPOSE 3306