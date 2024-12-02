#!/usr/bin/python

#
# Based on Deid Reimer's sample code
#

#
# DO NOT MODIFY THIS FILE
#

import sys
import time

# Read raw data from the 1-wire device file
def read_temp_raw(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

#
# DO NOT MODIFY THIS FILE
#

# Parse the raw data and extract the temperature
def read_temp(device_file):
	# Read raw lines until we get input that passes the address/code CRC check.
	lines = read_temp_raw(device_file)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw(device_file)

	# Find the position in the [1]th line string that contains the temperature 't='
	equals_pos = lines[1].find('t=')

	# If found then extract the temperature string
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

#
# DO NOT MODIFY THIS FILE
#

if __name__ == "__main__":
	# Ensure there are two arguments (the name of the executable and the temperature file)
	if len(sys.argv) != 2:
		sys.stdout.write("Missing temperature file\n")
		sys.exit(-1)

	# Read and display the current temperature
	try:
		temp = read_temp(sys.argv[1])
		sys.stdout.write(str(temp) + "C\n")
	except IOError as details:
		sys.stdout.write(str(details) + '\n')
		sys.exit(-1)
	except:
		sys.stdout.write("Unexpected error\n")
		sys.exit(-1)

#
# DO NOT MODIFY THIS FILE
#
