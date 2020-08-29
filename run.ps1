$Sample = Get-Random -Minimum -100 -Maximum 100
#$Sample2 = New-Guid
#echo $Sample2

#docker build --pull --no-cache --rm --build-arg URL='https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv' -f "csv2docker.dockerfile" -t csvtodockermysql:latest "."
docker build --pull --rm --build-arg URL='https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv' -f "csv2docker.dockerfile" -t csvtodockermysql:latest "."

docker run -i -t -d -p 3306:3306 --pid=host -v /var/lib/mysql --name mysql_container csvtodockermysql:latest
docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysql_container