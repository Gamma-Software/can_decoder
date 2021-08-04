*Date of creation: 29/03/2021*

# Gps measure
Parse the gps nmea and send via the mqtt server

## Requirements
pynmea
serial

# Installation
Create a python virtual environnement: 'virtualenv .venv"
Install requirements 'pip install -r requirements.txt'
Install the configurations and service and udev rule 'python3 (from the virtualenv) install.py'
Change default user and pass config in /etc/capsule/gps_measure/config.yaml

## Details
### Programming Language
This project is written in python and is meant to be run on a device that supports GPS queries.

### Integration
We assume that the script will only be run on Linux OS
TODO

# Mosquitto publish topics
process/gps_measure/alive
gps_measure/fixed
gps_measure/longitude
gps_measure/latitude
gps_measure/altitude
gps_measure/speed
gps_measure/route
