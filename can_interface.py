#!/usr/bin/python3
# This script will retrieve the raw data from the influx data from the last update,
# store the data in a custom sql database and generate the site

import io
import os
import yaml
import paho.mqtt.client as mqtt
import sys
import time
import logging
import datetime
import obd


# ----------------------------------------------------------------------------------------------------------------------
# Read script parameters
# ----------------------------------------------------------------------------------------------------------------------
path_to_conf = os.path.join("/etc/capsule/can_interface/config.yaml")
# If the default configuration is not install, then configure w/ the default one
if not os.path.exists(path_to_conf):
    sys.exit("Configuration file %s does not exists. Please reinstall the app" % path_to_conf)
# load configuration
with open(path_to_conf, "r") as file:
    conf = yaml.load(file, Loader=yaml.FullLoader)


# ----------------------------------------------------------------------------------------------------------------------
# Initiate MQTT variables
# ----------------------------------------------------------------------------------------------------------------------
# MQTT methods
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    obd.logging.info("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt

client = mqtt.Client()
logging.info("Connect to localhost broker")
client.username_pw_set(conf["mqtt"]["user"], conf["mqtt"]["pass"])
client.on_connect = on_connect  # Define callback function for successful connection
client.connect(conf["mqtt"]["host"], conf["mqtt"]["port"])
client.loop_start()

while not client.is_connected():
    logging.info("Waiting for the broker connection")
    time.sleep(1)


# ----------------------------------------------------------------------------------------------------------------------
# Initiate variables
# ----------------------------------------------------------------------------------------------------------------------
connected = False
obd.logger.setLevel(obd.logging.DEBUG if conf["debug"] else obd.logging.INFO) # enables all debug information
obd.logger.addHandler(logging.FileHandler("/var/log/capsule/can_interface.log", "a"))

# First Dump ELM Version
connection = obd.OBD(conf["can_interface"]["port"], conf["can_interface"]["baudrate"], start_low_power=False, fast=False)
obd.logging(connection.query(obd.commands.ELM_VERSION).value)

# Wait for the vehicle to switch on but monitor Battery Voltage though
try:
    command = obd.commands.ELM_VOLTAGE
    while connection.is_connected():
        client.publish("process/can_interface/alive", True)
        client.publish("can_interface/"+str(command), connection.query(command).value)
except KeyboardInterrupt:
    connection.close()
    logging.info("Stop script")
    sys.exit(0)


# TODO

# ----------------------------------------------------------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------------------------------------------------------
try:
    async_connection = obd.Async(conf["can_interface"]["port"], conf["can_interface"]["baudrate"], start_low_power=False, fast=False)

except KeyboardInterrupt:
    pass

logging.info("Stop script")
sys.exit(0)

exe
# a callback that prints every new value to the console
def new_rpm(r):
    print(r.value)


def value(r):
    print(r.value)
def watch_all_commands():
    for commands in list(connection.supported_commands):
        connection.watch(commands.name, callback=value)
        connection.start()

async_connection.watch(obd.commands.RPM, callback=new_rpm)
async_connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(60)
async_connection.stop()


exit(0)
while True and connection.is_connected():
    cmd = obd.commands.RPM # select an OBD command (sensor)
    response = connection.query(cmd) # send the command, and parse the response
    print(response.value) # returns unit-bearing values thanks to Pint
    time.sleep(1)

connection.close()