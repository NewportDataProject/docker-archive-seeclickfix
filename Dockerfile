FROM python:3

ENV GITHUB_USER=NDPGitBot

RUN apt-get update; apt-get install git
COPY make-archive.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY docker-entrypoint.sh .

ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
