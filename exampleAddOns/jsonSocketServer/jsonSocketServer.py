#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
jsonSocketServer
This is a small example of an jsonSocketServer for receive alarm-messages from BOSWatch.
The jsonSocketServer controlls an pibrella-bord in case of received POCSAG-RIC

Implemented functions:
- asynchronous service for alarm-sound
- green LED if jsonSocketServer is running
- green LED is blinking if Dau-Test-RIC was received
- yellow LED is blinking if our RICs is reveived with functioncode "a"
- red LED is blinking in case of an alarm (our RICs with functioncode "b")
- siren will run with the pack
- press Pibrella button to stop alarm and reset the LEDs

@author: Jens Herrmann

BOSWatch: https://github.com/Schrolli91/BOSWatch
Pibrella: https://github.com/pimoroni/pibrella
"""

# no IP for server necessary
IP = ""
# listen on port
PORT = 8112


import logging
import logging.handlers

import socket # for udp-socket
import pibrella # for pi-board
import json # for data


#
# Eventhandler for button
# will stop the alarm and reset the LEDs
#
def button_pressed(pin):
	global siren_stopped
	import pibrella
	pibrella.light.off()
	pibrella.light.green.on()
	siren_stopped = True
# load Eventhandler
pibrella.button.pressed(button_pressed)

#
# Siren-control
#

# normally we have no alarm, siren-control-var is True
siren_stopped = True

# asynchronous siren:
def siren():
	import time
	if siren_stopped == True:
		pibrella.buzzer.stop()
		return True
	for x in xrange(-30,30,2):
		pibrella.buzzer.note(x)
		time.sleep(0.01)
	for x in reversed(xrange(-30,30,2)):
		pibrella.buzzer.note(x)
		time.sleep(0.01)
# start asynchronous siren
pibrella.async_start('siren',siren)


#
# Main Program
#
try:
	# Logging
	myLogger = logging.getLogger()
	myLogger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(formatter)
	myLogger.addHandler(ch)

	# Start TCP socket:
	logging.debug("Start jsonSocketServer")
	sock = socket.socket()
	sock.bind((IP,PORT))
	sock.listen(2)
	logging.info("jsonSocketServer runs")
	pibrella.light.green.on()

	# our Alarm-RICs:
	ric_alarm = [12345677, 12345676, 12345675]

	while True:
		# accept connections from outside
		(clientsocket, address) = sock.accept()
		logging.debug("connected client: %s", address)

		# receive message as json string
		json_string = clientsocket.recv( 4096 ) # buffer size is 4096 bytes
		try:
			# parse json
			parsed_json = json.loads(json_string)
			logging.debug("parsed message: %s", parsed_json)
		except ValueError:
			# parsing error is foolish, but we don't have to exit
			logging.warning("No JSON object could be decoded: %s", json_string)
			pass
		else:
			# DAU-Test-RIC received
			if parsed_json['ric'] == "1234567":
				logging.debug("POCSAG is alive")
				pibrella.light.green.blink(1, 1)

			elif int(parsed_json['ric']) in ric_alarm:
				logging.debug("We have do to something")
				if parsed_json['functionChar'] == "a":
					logging.info("-> Probealarm: %", parsed_json['ric'])
					pibrella.light.yellow.blink(1, 1)
				elif parsed_json['functionChar'] == "b":
					logging.info("-> Alarm: %", parsed_json['ric'])
					pibrella.light.red.blink(1, 1)
					# change variable to False to start the siren
					siren_stopped = False

except KeyboardInterrupt:
	logging.warning("Keyboard Interrupt")
except:
	logging.exception("unknown error")
finally:
	try:
		logging.debug("socketServer shuting down")
		sock.close()
		logging.debug("socket closed")
		logging.debug("exiting socketServer")
	except:
		logging.warning("failed in clean-up routine")
	finally:
		logging.debug("close Logging")
		logging.info("socketServer exit()")
		logging.shutdown()
		ch.close()
		exit(0)
