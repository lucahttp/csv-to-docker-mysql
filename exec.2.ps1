$Sample = Get-Random -Minimum -100 -Maximum 100
#$Sample2 = New-Guid
#echo $Sample2

docker build --pull --no-cache --rm -f "2.dockerfile" -t csvtodockermysql:latest "."
docker run -i -t -d -p 3306:3306 --pid=host -v /var/lib/mysql --name mysql_container-$Sample csvtodockermysql:latest
docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysql_container-$Sample