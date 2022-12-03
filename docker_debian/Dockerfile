FROM python:3.8-buster

RUN apt-get update \
    && apt-get install -y python3-dev python3-psutil bluez bluez-hcidump sudo

WORKDIR /usr/src/app

COPY ./app/requirements.txt ./
COPY ./app/reporter.py ./
COPY ./app/app.py ./
COPY ./config.py ./
 
RUN python3 -m pip install --upgrade pip setuptools wheel && python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py" ]
