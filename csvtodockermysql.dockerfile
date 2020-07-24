FROM mysql:5.7

# ROOT PASSWORD
ENV MYSQL_ROOT_PASSWORD=mypassword

#ENV MYSQL_DATABASE=sampledb
ENV MYSQL_USER=sample-username
ENV MYSQL_PASSWORD=sapassword


ENV MYSQL_DATA_DIR=/var/lib/mysql \
    MYSQL_RUN_DIR=/run/mysqld \
    MYSQL_LOG_DIR=/var/log/mysql

RUN ["db_dump.sql", "/tmp/dump.sql"]

RUN /etc/init.d/mysql start && \
         mysql -u root -p$MYSQL_ROOT_PASSWORD  -e "GRANT ALL PRIVILEGES ON *.* TO 'comeon'@'%' IDENTIFIED BY 'password';FLUSH PRIVILEGES;" && \
        mysql -u root -p${MYSQL_ROOT_PASSWORD}  < /tmp/dump.sql

#PORT
EXPOSE 3306