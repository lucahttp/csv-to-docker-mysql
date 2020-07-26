FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root


COPY scripts/convert.sh /convert.sh
COPY scripts/init_db.sh /docker-entrypoint-initdb.d/

RUN csv-sql.sh <filename>.csv


#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

