FROM salicml/requirements:latest

COPY tasks.py /tasks.py
COPY etc/ /etc/

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
        echo $TZ > /etc/timezone && \
        dpkg-reconfigure -f noninteractive tzdata

ADD etc/scripts/crontab /etc/cron.d/complexity-cron

RUN chmod 0644 /etc/cron.d/complexity-cron && \
        touch /var/log/cron_complexity.log && \
        crontab /etc/cron.d/complexity-cron


