# ble-gateway

Raspberry pi gateway for BLE sensors. Work in progress.

## Status

* runs locally on debian stretch, Python 3.5, built-in bluetooth
* run in debian stretch based Python 3.5. docker container (some magic required to start, see bottom)
* runs together with balena wifi connect (see `balena_wificonnect` directory)
* testing git hooks

## TODO / next steps

* use environment variables or a JSON config to pass all sensitive information. Would also make changing endpoints easy.


# Howto

Uses libarary:

https://pypi.org/project/ruuvitag_sensor/


## Local development

### Install required packages

OS level packages:
```` bash
sudo apt-get install bluez bluez-hcidump
````

Python environment:
```` bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate

python3 -m pip install wheel ruuvitag_sensor
````


### To run the examples

```` bash
sudo ../venv/bin/python3 ruuvi_app_multitag.py  
````

BLE tools require sudo. Explicit reference to venv's python executable is needed for running the code with sudo privileges.


## Local development with Docker

Files under app/ need to be copied to the same directory as the Dockerfile for the docker build to work. Master versions of the files reside in app/.

### Step 1

Check the [./docker_debian/config.py](./docker_debian/config.py) contents and modify if needed.

### Step 2

Run these to test or deploy:

```` bash
cp app/*.* docker_debian/app
docker compose build
docker compose up -d
````
This is the recommended way as the `docker-compose.yml` e.g. sets logging such that the log files will not grow without limit.

To run without docker compose:
```` bash
cp app/*.* docker_debian/app
cd docker_debian

docker build -t gwtest .
sudo docker run -d --net=host --privileged -i -t gwtest

docker build -t ble-gateway .
sudo docker run -d --restart=always --net=host --privileged -i -t ble-gateway

````



Other docker commands that might be of help in some environments:
```` bash
sudo docker run --cap-add=SYS_ADMIN -v /opt/bluetooth:/var/lib/bluetooth -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /tmp/$(mktemp -d):/run --net=host --privileged -i -t gwtest /bin/bash

sudo docker run --net=host --privileged -i -t gwtest /bin/bash
````


## Deploy to balena device

Install balena command line tool. Then:

```` bash
balena login
mkdir balena_basic/
cp app/*.* balena_basic/app
cp app/config_prod.py balena_basic/app/config.py
cd balena_basic
balena push BLE-gateway # OR
balena push BLE-gateway-test
````

```` bash
balena login

cp app/*.* docker_debian/
cd docker_debian
balena push BLE-gateway
````

The Dockerfile should be named `Dockerfile.template`: otherwise balena push command doesn't fetch the base image correctly.
Files under `balena_wificonnect` are copies from `app` as files to copy need to be in the same directory structure as the Dockerfile and symlinks do not work (?).

# Changelog

2022-09-11 Added three new ruuvi tag mac addresses
2021-06-19 Upgraded balena wifi-connect. Now using debian from balena container images as the base. Balena python example was outdated.
2021-01-23 Changed to python:3.8-buster in Dockerfile due to pip install problems. Improved pip installation commands as well.