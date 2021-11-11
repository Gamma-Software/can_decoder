import obd

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
connection = obd.OBD("/dev/rfcomm0", 38400,check_voltage=False,  start_low_power=False, fast=False)


cmd = obd.commands.ELM_VOLTAGE # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value.magnitude) # returns unit-bearing values thanks to Pint

connection.close()