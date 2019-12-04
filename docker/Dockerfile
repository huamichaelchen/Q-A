FROM tomcat:8.0

RUN apt-get update && apt-get install cron python3 vim -y

COPY tomfinder-cron /etc/cron.d/tomfinder-cron 
RUN chmod 0644 /etc/cron.d/tomfinder-cron && crontab /etc/cron.d/tomfinder-cron

WORKDIR /tomfinder

CMD ["/bin/bash"]
