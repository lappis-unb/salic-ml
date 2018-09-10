FROM debian:buster-slim

WORKDIR /salic-ml

RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    python3-pip \
    unixodbc-dev

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

ADD . /salic-ml/

RUN pip install -r requirements.txt
RUN python setup.py develop

ENV LC_ALL C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 8888

ENTRYPOINT ["./docker/entrypoint.sh"]
