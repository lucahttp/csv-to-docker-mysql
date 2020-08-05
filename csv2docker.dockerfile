FROM mysql

#COPY files/init_db.sh /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD root
RUN apt update
RUN apt install wget
#COPY scripts/convert2.sh /convert.sh
#COPY scripts/my.csv /my.csv
RUN  mkdir  /csv2sql/
COPY scripts/ /csv2sql/
RUN ls /csv2sql/
#ADD scripts /csv2sql/

#RUN for file in /csv2sql/* do cat "$file" >> results.out done

RUN for file in /csv2sql/* ; do echo "hello $file"; done

# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory

# https://stackoverflow.com/questions/26504846/copy-directory-to-other-directory-at-docker-using-add-command

WORKDIR /csv2sql/

#RUN for i in *.csv; do echo "hello $i"; done

RUN for i in *.csv; do /csv2sql/convert.sh $i ; done

#RUN for file in /csv2sql/* ; do echo "hello $file"; done

#RUN /csv2sql/convert.sh /csv2sql/my.csv
RUN ls /csv2sql/

#RUN sed '1iCREATE DATABASE DatabaseName;' my.sql
#RUN sed '2iUSE DatabaseName;' my.sql

RUN for i in *.sql; do cp $i /docker-entrypoint-initdb.d/ ; done


#https://unix.stackexchange.com/questions/438105/remove-certain-characters-in-a-text-file
#sed -e 's/.*]//' -e 's/  */ /g' file.txt

#RUN cp /csv2sql/my.sql /docker-entrypoint-initdb.d/

#RUN echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION" > /my2.sql

# https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
# https://github.com/docker-library/mysql/issues/129
RUN echo "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;" > /csv2sql/my2.sql

RUN cp /csv2sql/my2.sql /docker-entrypoint-initdb.d/

#RUN /etc/init.d/mysql start
#RUN mysql -u root -p -e "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION"

#RUN sed -i -e 's/\r$//' /docker-entrypoint-initdb.d/init_db.sh
#COPY ./files/epcis_schema.sql /tmp/

#RUN mysqlimport  --ignore-lines=1 --fields-terminated-by=, --columns='ID,Name,Phone,Address' --local -u root -p Database /path/to/csvfile/TableName.csv

EXPOSE 3306