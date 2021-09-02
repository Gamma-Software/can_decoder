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
async_connection = obd.Async(conf["can_interface"]["port"], conf["can_interface"]["baudrate"], start_low_power=False, fast=False)
obd.logging.info(connection.query(obd.commands.ELM_VERSION).value)

try:
    # ----------------------------------------------------------------------------------------------------------------------
    # Main loop
    # ----------------------------------------------------------------------------------------------------------------------
    while True:
        # Wait for the vehicle to switch on but monitor Battery Voltage though
        try:
            command = obd.commands.ELM_VOLTAGE
            while not connection.is_connected():
                client.publish("process/can_interface/alive", True)
                client.publish("can_interface/"+str(command), connection.query(command).value)
                time.sleep(2) # No need to rush
        except KeyboardInterrupt:
            break
        
        obd.logging.info("The contact key is switched ON")

        def publish_command_result(c, r):
            client.publish("can_interface/"+str(c), r)
        
        try:
            # Initiate all callbacks
            for commands in list(connection.supported_commands):
                async_connection.watch(commands.name, callback=publish_command_result)
                async_connection.start()
            # keep monitoring until the car is switched off
            while async_connection.is_connected() and async_connection.running:
                client.publish("process/can_interface/alive", True)
                time.sleep(conf["period_s"])
        except KeyboardInterrupt:
            break
except KeyboardInterrupt:
    pass

connection.close()
async_connection.close()
obd.logging.info("Stop script")
client.publish("process/can_interface/alive", False)
sys.exit(0)
