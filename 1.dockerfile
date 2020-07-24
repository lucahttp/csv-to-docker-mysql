FROM ubuntu:latest
 
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server \
 && sed -i "s/127.0.0.1/0.0.0.0/g" /etc/mysql/mysql.conf.d/mysqld.cnf \
 && mkdir /var/run/mysqld \
 && chown -R mysql:mysql /var/run/mysqld
 
VOLUME ["/var/lib/mysql"]
 
EXPOSE 3306
 
CMD ["mysqld_safe"]
#http://www.inanzzz.com/index.php/post/w4i9/running-mysql-server-as-foreground-on-ubuntu-with-dockerfile

#docker build --pull --rm -f "1.dockerfile" -t csvtodockermysql:latest "."
#docker run -i -t -d --name mysql_container csvtodockermysql:latest


#docker build -t mysql_image .
#docker run -i -t -d --name mysql_container mysql_image