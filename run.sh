#$Sample = Get-Random -Minimum -100 -Maximum 100
#$Sample2 = New-Guid
#echo $Sample2

docker build --pull --no-cache --rm -f "csv2docker.dockerfile" -t csv2docker:latest "."
docker run -i -t -d -p 3306:3306 --pid=host -v /var/lib/mysql --name csv2docker csv2docker:latest
#docker inspect --format '{{ .NetworkSettings.IPAddress }}' csv2docker