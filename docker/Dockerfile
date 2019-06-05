FROM salicml/requirements:latest

COPY tasks.py /tasks.py
COPY etc/ /etc/
COPY src/ src/

RUN rm -f /etc/localtime
RUN ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

ADD etc/scripts/crontab /etc/cron.d/complexity-cron

LABEL com.centurylinklabs.watchtower.enable="true"

RUN touch /var/log/test_log.log

RUN chmod 0644 /etc/cron.d/complexity-cron && \
        touch /var/log/cron_complexity.log && \
        crontab /etc/cron.d/complexity-cron


