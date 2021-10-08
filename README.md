*Date of creation: 04/08/2021*

# Can decoder
Decode CAN frame of the Capsule car (Toyota Hilux) via OBD-II interface

# Installation
1. Create a python virtual environnement: 'virtualenv .venv" and activate it
2. Install requirements 'pip install -r requirements.txt'
3. Install the configurations and service and udev rule (from the virtualenv) 'python3 install.py'
4. Change default user and pass config in /etc/capsule/can_decoder/config.yaml

# Details
## Integration
* This project is tested and developed to be used on a Toyota Hilux.\
* To make it work you should by a OBD-II adapter. Tested on a bluetooth adapter but via USB it should work.\
* To share the data we use the Mosquito framework

## Docker
You can start the script with Docker with the command:
docker run -v path/to/config.yaml:/etc/capsule/can_interface/config.yaml:ro --privileged -p 1884:1884 -p 8086:8086 can_decoder
