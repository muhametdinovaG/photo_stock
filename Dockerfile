FROM python:3.6-alpine

COPY . /usr/local/stock

COPY worker.sh /etc/periodic/daily
RUN chmod +x /etc/periodic/daily/worker.sh

CMD ["crond", "-l", "2", "-f"]