docker build --pull --rm -f "1.dockerfile" -t csvtodockermysql:latest "."
docker run -i -t -d -p 3306:3306 --pid=host --name mysql_container csvtodockermysql:latest
docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysql_container