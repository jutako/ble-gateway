FROM python:3.8-buster

RUN apt-get update \
    && apt-get install -y python3-dev python3-psutil bluez bluez-hcidump sudo

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY reporter.py ./
COPY app.py ./
 
RUN python3 -m pip install --upgrade pip && python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py" ]
