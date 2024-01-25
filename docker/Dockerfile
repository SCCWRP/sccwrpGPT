# sccwrp/flask:ai-search
FROM debian:buster-slim

WORKDIR /home

# Libs to compile and install python, and others
RUN apt-get update
RUN apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev 
RUN apt-get install -y wget xz-utils uwsgi vim 

# For Postgres Libs - psycopg2 and sqlalchemy
RUN apt-get install -y libpq-dev gcc


# Install Python 3.8.8
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz
RUN tar -xf Python-3.8.8.tgz
WORKDIR /tmp/Python-3.8.8
RUN ./configure --enable-optimizations
RUN make -j 2
RUN make install
WORKDIR /tmp
RUN rm -rf Python-3.8.8/
RUN rm Python-3.8.8.tgz
WORKDIR /home

# Order matters here
# libs that i know have breaking changes are sqlalchemy, pandas and the OpenAI API for Python
RUN pip3 install ipython
RUN pip3 install openai==1.9.0
RUN pip3 install psycopg2
RUN pip3 install "sqlalchemy<2.0.0"
RUN pip3 install flask
RUN pip3 install "pandas<2.0.0" 

# For running the flask app - i think
RUN pip3 install uwsgi

# Because i thought requests was in the PSL
RUN pip3 install requests

