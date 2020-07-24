FROM ubuntu:latest
 
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server \
 && sed -i "s/127.0.0.1/0.0.0.0/g" /etc/mysql/mysql.conf.d/mysqld.cnf \
 && mkdir /var/run/mysqld \
 && chown -R mysql:mysql /var/run/mysqld
 


#RUN mysql -u root -p -e "UPDATE user SET Password=PASSWORD('YOURNEWPASSWORD') WHERE User='root'; FLUSH PRIVILEGES; exit;"
#RUN mysql -u root -e "UPDATE user SET Password=PASSWORD('YOURNEWPASSWORD') WHERE User='root'; FLUSH PRIVILEGES; exit;"
VOLUME ["/var/lib/mysql"]

#RUN echo 'root' | passwd root --stdin
RUN echo root:root | chpasswd
EXPOSE 3306
 
CMD ["mysqld_safe"]
#http://www.inanzzz.com/index.php/post/w4i9/running-mysql-server-as-foreground-on-ubuntu-with-dockerfile

#docker build --pull --rm -f "1.dockerfile" -t csvtodockermysql:latest "."
#docker run -i -t -d --name mysql_container csvtodockermysql:latest



#docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysql_container

#docker build -t mysql_image .
#docker run -i -t -d --name mysql_container mysql_image