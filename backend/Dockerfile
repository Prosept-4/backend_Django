FROM python:3.11-slim

LABEL description="Procept hakathon team 4: Backend" \
      version="1.0.0" \
      maintainer="Team 4" \
      deployers="https://github.com/KirillShirokov | https://github.com/PrimeStr"

RUN apt-get update && \
    apt-get install -y dos2unix

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
COPY requirements-DS.txt .

RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -r requirements-DS.txt --no-cache-dir

RUN pip install spacy==3.7.2

RUN python -m spacy download ru_core_news_sm
RUN python -m spacy download en_core_web_sm

COPY . .

RUN dos2unix run_django.sh

CMD ["bash", "run_django.sh"]
