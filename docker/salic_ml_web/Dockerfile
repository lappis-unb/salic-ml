FROM debian:buster-slim

EXPOSE 8080

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-crypto \
        python3-setuptools \
        python3-pyodbc \
        tdsodbc \
        unixodbc-dev \
        # libmysqlclient-dev \
        unixodbc \
        freetds-dev \
        cron

RUN apt-get install --reinstall -y locales tzdata && \
        sed -i 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
        locale-gen pt_BR.UTF-8

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR
ENV LC_ALL pt_BR.UTF-8
ENV TZ=America/Sao_Paulo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
        echo $TZ > /etc/timezone && \
        dpkg-reconfigure -f noninteractive tzdata

ADD etc/scripts/crontab /etc/cron.d/complexity-cron

RUN chmod 0644 /etc/cron.d/complexity-cron && \
        touch /var/log/cron_complexity.log && \
        crontab /etc/cron.d/complexity-cron

RUN mkdir /api

ADD . /api/

ADD etc/scripts/odbcinst.ini /etc/odbcinst.ini

WORKDIR /api

RUN ls

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
