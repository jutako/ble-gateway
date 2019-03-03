FROM balenalib/rpi-alpine-python:3.7.2-edge-build

# linux-headers: for e.g. types.h
#
# Some packages required by ruuvitag_sensor library are named differently uder alpine:
# python3-psutil -> py3-psutil
#
# Not available for alpine:
#     bluez-hcidump \
RUN apk update \
    && apk upgrade \
    && apk add linux-headers sudo openrc python3-dev py3-psutil bluez bluez-hid2hci py3-bluez \
    && rc-update add bluetooth



COPY app.py /app/
WORKDIR /app
CMD [ "python", "./app.py" ]