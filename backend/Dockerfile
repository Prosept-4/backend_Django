FROM python:3.11-slim

LABEL description="Procept hakathon team 4: Backend" \
      version="1.0.0" \
      maintainer="Team 4" \
      deployer="https://github.com/KirillShirokov | https://github.com/PrimeStr"

RUN apt-get update && \
    apt-get install -y dos2unix

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN dos2unix run_django.sh

CMD ["bash", "run_django.sh"]
