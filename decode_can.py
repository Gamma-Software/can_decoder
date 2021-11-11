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
from obd import OBDStatus


# ----------------------------------------------------------------------------------------------------------------------
# Read script parameters
# ----------------------------------------------------------------------------------------------------------------------
path_to_conf = os.path.join("/etc/capsule/can_decoder/config.yaml")
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
obd.logger.addHandler(logging.FileHandler("/var/log/capsule/can_decoder.log", "a"))

# First Dump ELM Version
connection = obd.OBD(conf["can_decoder"]["port"], conf["can_decoder"]["baudrate"], check_voltage=False, start_low_power=False, fast=False)
obd.logging.info(connection.query(obd.commands.ELM_VERSION).value)

# Get wanted commands
wanted_commands = {}
with open("wanted_commands.txt") as f:
    lines = f.readlines()
    for i, r in enumerate(lines): 
        wanted_commands[r.strip("\n").split(",")[0]] = r.strip("\n").split(",")[1]

try:
    # ----------------------------------------------------------------------------------------------------------------------
    # Main loop
    # ----------------------------------------------------------------------------------------------------------------------
    # Wait for the vehicle to switch on but monitor Battery Voltage though
    command = obd.commands.ELM_VOLTAGE
    response = connection.query(command) # This prevented from receiving None at first query (idk why)
    voltage = 0.0
    while voltage < 13.5:
        client.publish("process/can_decoder/alive", True)
        response = connection.query(command)
        try:
            voltage = response.value.magnitude
            client.publish("can_decoder/"+str(command.name), voltage)
        except ValueError as e:
            print("Error in result command / ", e)
            break
        except AttributeError as e:
            print("Error in result command / ", e)
            break
        time.sleep(2) # No need to rush

    obd.logging.info("The contact key is switched ON and the engine started, wait 2 seconds to connect")
    connection.close() # Close initial connection
    time.sleep(2)
    connection = obd.Async(conf["can_decoder"]["port"], conf["can_decoder"]["baudrate"], check_voltage=False, start_low_power=False, fast=False)
    def publish_command_result(c, r):
        if c.name == "ELM_VOLTAGE" and r.value.magnitude < 13.0:
            connection.close()
            obd.logging.info("Stop script")
            client.publish("process/can_decoder/alive", False)
            sys.exit(0)

        try:
            # Expose value (striped of its unit) through mqtt network 
            client.publish("can_decoder/"+str(c.name), r.value.magnitude)
        except ValueError as e:
            print("Error in result command / ", e)
            pass
        except AttributeError as e:
            print("Error in result command / ", e)
            pass

    while True:
        # Initiate all callbacks if supported and wanted
        for supported_command in list(connection.supported_commands):
            if supported_command.name in list(wanted_commands.keys()):
                connection.watch(supported_command, callback=publish_command_result)
        connection.start()
        try:
            # keep monitoring until the car is switched off
            while connection.is_connected() and connection.running:
                client.publish("process/can_decoder/alive", True)
                time.sleep(conf["period_s"])
        except KeyboardInterrupt:
            break
        connection.stop()
        connection.unwatch_all()
except KeyboardInterrupt:
    pass

connection.close()
obd.logging.info("Stop script")
client.publish("process/can_decoder/alive", False)
sys.exit(0)
