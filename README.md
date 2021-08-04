*Date of creation: 04/08/2021*

# Can decoder
Decode CAN frame of the Capsule car (Toyota Hilux) via OBD-II interface and a python library

## Requirements
python-can
paho
pyyaml

# Installation
Create a python virtual environnement: 'virtualenv .venv"
Install requirements 'pip install -r requirements.txt'
Install the configurations and service and udev rule 'python3 (from the virtualenv) install.py'
Change default user and pass config in /etc/capsule/can_decoder/config.yaml

## Details
### Integration
We assume that the script will only be run on Linux OS
TODO

# Mosquitto publish topics
process/can_decoder/alive
can_decoder/speed
can_decoder/rpm
can_decoder/motor_temperature
