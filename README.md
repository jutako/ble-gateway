# ble-gateway
Raspberry pi gateway for BLE sensors. Work in progress.

## Status

* runs locally on debian stretch, Python 3.5, built-in bluetooth
* run in debian stretch based Python 3.5. docker container (some magic required to start, see bottom)
* runs together with balena wifi connect (see `balena_wificonnect` directory)
* testing git hooks

## TODO / next steps

* use environment variables or a JSON config to pass all sensitive information
* connect balena app to repo


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

```` bash
docker build -t gwtest .
sudo docker run -d --net=host --privileged -i -t gwtest
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
cp app/*.* balena_wificonnect/app
cd balena_wificonnect
balena push BLE-gateway
````

The Dockerfile should be named `Dockerfile.template`: otherwise balena push command doesn't fetch the base image correctly.
Files under `balena_wificonnect` are copies from `app` as files to copy need to be in the same directory structure as the Dockerfile and symlinks do not work (?).
