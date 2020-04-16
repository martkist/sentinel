FROM debian:stretch-slim

RUN apt-get update
RUN apt-get install -y python-virtualenv git watch cron

RUN git clone https://github.com/martkist/sentinel.git /sentinel

WORKDIR /sentinel

RUN virtualenv ./venv
RUN ./venv/bin/pip install -r requirements.txt

COPY cronjobs /var/spool/cron/crontabs/root
RUN chmod 0600 /var/spool/cron/crontabs/root

COPY entrypoint.sh /sentinel/entrypoint.sh
RUN chmod +x /sentinel/entrypoint.sh
ENTRYPOINT ["/sentinel/entrypoint.sh"]