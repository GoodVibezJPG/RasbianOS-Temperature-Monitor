#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import temperature

#
# Replace the blank below with your device file
#
DEVICE_FILE = "/sys/devices/w1_bus_master1/10-0008032703f8/w1_slave"
TEMPERATURE_DATA = "/home/cirvine/Web_Temp/temperature.txt"

# GPIO setup for LEDs
RED_LED = 18    # GPIO pin for red LED
GREEN_LED = 22  # GPIO pin for green LED
YELLOW_LED = 27 # GPIO pin for yellow LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)

GPIO.output(RED_LED, GPIO.LOW)
GPIO.output(GREEN_LED, GPIO.LOW)
GPIO.output(YELLOW_LED, GPIO.LOW)

HTML_START = """
<html>
<head>
	<meta http-equiv="refresh" content="5">
	<title>Current Temperature</title>
</head>
<body>
"""

HTML_END = """
</body>
</html>
"""

def application(env, start_response):
	status = "200 OK"
	headers = [("Content-type", "text/html")]
	start_response(status, headers)
	body = HTML_START

	try:
		current_temp = temperature.read_temp(DEVICE_FILE)
		body += "It is currently " + str(current_temp) + "&degC\n"
		previous_temp = read_temp(TEMPERATURE_DATA)
		body += "It was previously " + str(previous_temp) + "&degC\n"
		body += "Temperature is ...\n"
		
		if current_temp > previous_temp:
			body += "Rising\n"
			GPIO.output(RED_LED, GPIO.HIGH)
			GPIO.output(GREEN_LED, GPIO.LOW)
			GPIO.output(YELLOW_LED, GPIO.LOW)
		if current_temp < previous_temp:
			body += "Falling\n"
			GPIO.output(GREEN_LED, GPIO.HIGH)
			GPIO.output(RED_LED, GPIO.LOW)
			GPIO.output(YELLOW_LED, GPIO.LOW)
		if current_temp == previous_temp:
			body += "Unchanged\n"
			GPIO.output(YELLOW_LED, GPIO.HIGH)
			GPIO.output(RED_LED, GPIO.LOW)
			GPIO.output(GREEN_LED, GPIO.LOW)

		write_temp(current_temp, TEMPERATURE_DATA)

	finally:
		body += HTML_END
		GPIO.cleanup()

	yield bytes(body, encoding='utf-8')

def write_temp(current_temp, TEMPERATURE_DATA):
	f = open(TEMPERATURE_DATA, "w")
	f.write(str(current_temp))
	f.close()

def read_temp(TEMPERATURE_DATA):
	f = open(TEMPERATURE_DATA, "r")
	temp = f.read()
	f.close()
	
	try:
		return float(temp)
	
	except ValueError:
		return 0.0

