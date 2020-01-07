FROM python:3.5-stretch

RUN apt-get update \
    && apt-get install -y python3-dev python3-psutil bluez bluez-hcidump sudo

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY reporter.py ./
COPY app.py ./
 
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py" ]