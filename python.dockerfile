FROM python:3.8-slim
ARG URL="https://people.sc.fsu.edu/~jburkardt/data/csv/grades.csv" 
ENV URL "https://gist.githubusercontent.com/lukaneco/2f321eb14e926b63521c5eb30cb0b11c/raw/ff413ac9d813914a2bdaf46abf58a9362efbb6f8/example.csv"

ARG MYSQL_DATABASE="mydatabase"
ARG MYSQL_USER="admin"
ARG MYSQL_PASSWORD="admin"
#ENV DATASOURCEFILE="mycsvfile.csv"
RUN apt update -y
RUN apt install wget -y
# set the working directory in the container
#RUN mkdir /app
WORKDIR /app
# copy the dependencies file to the working directory
COPY requirements.txt .
# install dependencies
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
# copy the content of the local src directory to the working directory

#RUN wget -nd -np -P /app/ --recursive ${URL}

COPY server.py .
ENTRYPOINT ["python"]
#CMD ["server.py"]
#CMD ["server.py", "-u", "https://gist.githubusercontent.com/lukaneco/2f321eb14e926b63521c5eb30cb0b11c/raw/ff413ac9d813914a2bdaf46abf58a9362efbb6f8/example.csv"]
CMD ["server.py", "-u", "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv"]
#CMD ["server.py", "-u", "'$URL'"]