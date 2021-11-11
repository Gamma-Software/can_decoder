import obd
import time

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
connection = obd.Async("/dev/rfcomm0", 38400, start_low_power=False, fast=False, delay_cmds=1.0)

print(connection.status()) # returns unit-bearing values thanks to Pint

print(connection.is_connected())


def publish_command_result(c, r):
    try:
        print("can_decoder/"+str(c).split(":", 1)[1], r)
    except ValueError as e:
        print("Error in result command / ", e)

try:
    # Initiate all callbacks
    connection.watch(obd.commands.RPM, callback=publish_command_result)
    connection.watch(obd.commands.SPEED, callback=publish_command_result)
    if connection.start():
        time.sleep(60)
    # keep monitoring until the car is switched off
    #while connection.is_connected():
    #    time.sleep(1)
except KeyboardInterrupt:
    pass

connection.close()