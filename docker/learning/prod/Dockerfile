FROM debian:buster-slim

RUN mkdir /salic-ml
WORKDIR /salic-ml

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-pyodbc \
        tdsodbc \
        unixodbc \
        unixodbc-dev \
        freetds-dev \
        build-essential

RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

ADD ./setup.py /salic-ml/
ADD ./requirements.txt /salic-ml/
ADD ./docker/odbcinst.ini /etc/odbcinst.ini

RUN pip3 install -r requirements.txt
RUN python3 setup.py develop

ADD . /salic-ml/

EXPOSE 8080
ENV FLASK_ENV=development
ENV FLASK_APP=/salic-ml/salicml/api/main.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--debugger"]
