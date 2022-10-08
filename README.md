# ble-gateway

Raspberry pi gateway for BLE sensors. Work in progress.

## Status

* runs locally on debian stretch, Python 3.5, built-in bluetooth
* run in debian stretch based Python 3.5. docker container (some magic required to start, see bottom)
* runs together with balena wifi connect (see `balena_wificonnect` directory)
* testing git hooks

# Howto

Uses library:

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

Add the server and database to app.py

### Step 2

Run these to test or deploy:

```` bash
cp app/*.* docker_debian/
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

# Known issues

## Deprecated hcitool

It seems Linux hcitool has not been maintained in several years. On Tuxedo OS 22.04 (jammy) hcitool gives error:
```
jkor@tux:~$ sudo hcitool lescan
Set scan parameters failed: Input/output error
```

Another option is to use the cross platform BLE adapters, such as Bleak. However, the asyncio example given on https://github.com/ttu/ruuvitag-sensor worked only on latest ruuvitag-sensor installed from github:
 ```
python -m pip install -U git+https://github.com/ttu/ruuvitag-sensor
 ```

Especially it did not work on ruuvitag-sensor==2.0.0 from pypi.
# TODO

* use environment variable to set gateway name/id
* use environment variables or a JSON config to pass all sensitive information. Would also make changing endpoints easy.
* collect all configurations to same file as dict. Select environment using environment variable or command line paramenter.
* configure local development with venv
* configure local development with docker
* add docker-compose.yaml files for ease of configuration for multicontainer use
* add support for http API data output
* document testing and deployment to balena
* how to add as one container to a multicontainer balena project
* use logging module

# Changelog

2022-09-11 Added three new ruuvi tag mac addresses
2021-06-19 Upgraded balena wifi-connect. Now using debian from balena container images as the base. Balena python example was outdated.
2021-01-23 Changed to python:3.8-buster in Dockerfile due to pip install problems. Improved pip installation commands as well.