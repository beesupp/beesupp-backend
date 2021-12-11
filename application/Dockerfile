FROM python:3.9

RUN apt-get -y update && \
    apt-get install -y netcat && \
    apt-get install -y dos2unix

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

# sometimes git cloning the project makes the .sh scripts lien ending as CRLF and it causes crash on the debian based environment, convert them to LF
RUN dos2unix /app/wait-for-db.sh

# make it exec
RUN chmod +x /app/wait-for-db.sh

CMD ["/bin/bash", "/app/wait-for-db.sh", "python", "app.py"]