#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
alarmMonitor

This is an alarmMonitor for receive alarm-messages from BOSWatch and show them on a touchscreen
The jsonSocketServer controlls an Watterott RPi-Display in case of received POCSAG-RIC

Implemented functions:
- asynchronous threads for display control
- show ric-description and alarm-message on display
- different colours for no alarm, test alarm and alarm
- auto-turn-off display
- show POCSAG is alive status (coloured clock)

@author: Jens Herrmann

BOSWatch:    https://github.com/Schrolli91/BOSWatch
RPi-Display: https://github.com/watterott/RPi-Display
"""

import logging
import logging.handlers
import ConfigParser

import os
import time
import socket # for socket
import json # for data
from threading import Thread
import pygame # for building colour-tuple

import globals

try: 
	#
	# Logging
	#
	myLogger = logging.getLogger()
	myLogger.setLevel(logging.DEBUG)
	# set log string format
	formatter = logging.Formatter('%(asctime)s - %(module)-24s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
	# create a display logger
	ch = logging.StreamHandler()
	# log level for display >= info
	ch.setLevel(logging.INFO) 
	#ch.setLevel(logging.DEBUG) 
	ch.setFormatter(formatter)
	myLogger.addHandler(ch)		

	#
	# Read config.ini
	#
	try:
		logging.debug("reading config file")
		globals.config = ConfigParser.SafeConfigParser()
		globals.config.read("config.ini")
		# if given loglevel is debug:
		for key,val in globals.config.items("AlarmMonitor"):
			logging.debug(" -- %s = %s", key, val)
	except:
		# we couldn't work without config -> exit
		logging.critical("cannot read config file")
		logging.debug("cannot read config file", exc_info=True)
		exit(1)
	
	#
	# set environment for display and touchscreen
	#
	os.environ["SDL_FBDEV"] = "/dev/fb1"
	os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
	os.environ["SDL_MOUSEDRV"] = "TSLIB"

	#
	# start threads 
	#
	try:
		from displayServices import displayPainter, autoTurnOffDisplay, eventHandler
		globals.screenBackground = pygame.Color(globals.config.get("AlarmMonitor","colourGreen"))
		logging.debug("Start displayPainter-thread")
		Thread(target=displayPainter).start()
		logging.debug("Start autoTurnOffDisplay-thread")
		Thread(target=autoTurnOffDisplay).start()
		logging.debug("Start eventHandler-thread")
		Thread(target=eventHandler).start()
	except:
		# we couldn't work without config -> exit
		logging.critical("cannot start displayService-Threads")
		logging.debug("cannot start displayService-Threads", exc_info=True)
		exit(1)

	#
	# start socket
	#
	logging.debug("Start socketServer")
	sock = socket.socket () # TCP
	sock.bind(("",globals.config.getint("AlarmMonitor","socketPort")))
	sock.listen(5)
	logging.info("socketServer runs")

	#
	# Build Lists out of config-entries
	#
	logging.debug("create lists")
	keepAliveRICs         = [int(x.strip()) for x in globals.config.get("AlarmMonitor","keepAliveRICs").replace(";", ",").split(",")]
	logging.debug("-- keepAliveRICs: %s", keepAliveRICs)
	alarmRICs             = [int(x.strip()) for x in globals.config.get("AlarmMonitor","alarmRICs").replace(";", ",").split(",")]
	logging.debug("-- alarmRICs: %s", alarmRICs)
	functionCharTestAlarm = [x.strip() for x in globals.config.get("AlarmMonitor","functionCharTestAlarm").replace(";", ",").split(",")]
	logging.debug("-- functionCharTestAlarm: %s", functionCharTestAlarm)
	functionCharAlarm     = [x.strip() for x in globals.config.get("AlarmMonitor","functionCharAlarm").replace(";", ",").split(",")]
	logging.debug("-- functionCharAlarm: %s", functionCharAlarm)
	
	#
	# Main Program
	# (Threads will set abort to True if an error occurs)
	#
	while globals.abort == False:
		# accept connections from outside
		(clientsocket, address) = sock.accept()
		logging.debug("connected client: %s", address)

		# recv message as json_string
		json_string = clientsocket.recv( 4096 ) # buffer size is 1024 bytes
		try:
			# parsing jason
			parsed_json = json.loads(json_string)
			logging.debug("parsed message: %s", parsed_json)
		except ValueError:
			# we will ignore waste in json_string
			logging.warning("No JSON object could be decoded: %s", json_string)
			pass
		else:
			try:
				logging.debug("Alarmmessage arrived")
				logging.debug("-- ric: %s", parsed_json['ric'])
				logging.debug("-- functionChar: %s", parsed_json['functionChar'])
				# keep alive calculation with additional RICs
				if parsed_json['ric'] in keepAliveRICs:
					logging.info("POCSAG is alive")
					globals.lastAlarm = int(time.time())

				# (test) alarm processing
				elif parsed_json['ric'] in alarmRICs:
					logging.debug("We have do to something")
					if parsed_json['functionChar'] in functionCharTestAlarm:
						logging.info("-> Probealarm: %s", parsed_json['ric'])
						globals.screenBackground = pygame.Color(globals.config.get("AlarmMonitor","colourYellow"))
					elif parsed_json['functionChar'] in functionCharAlarm:
						logging.info("-> Alarm: %s", parsed_json['ric'])
						globals.screenBackground = pygame.Color(globals.config.get("AlarmMonitor","colourRed"))
						
					# forward data to alarmMonitor
					globals.data = parsed_json
					# update lastAlarm for keep alive calculation
					globals.lastAlarm = int(time.time())
					# enable display for n seconds:
					globals.enableDisplayUntil = int(time.time()) + globals.config.getint("AlarmMonitor","showAlarmTime")
					# tell alarm-thread to turn on the display
					globals.showDisplay = True;
					
			except KeyError:
				# we will ignore waste in json_string
				logging.warning("No RIC found: %s", json_string)
				pass
	
except KeyboardInterrupt:
	logging.warning("Keyboard Interrupt")	
except:
	logging.exception("unknown error")
finally:
	try:
		logging.info("socketServer shuting down")
		globals.running = False
		sock.close()
		time.sleep(0.5)
		logging.debug("socket closed") 
		logging.debug("exiting socketServer")		
	except:
		logging.warning("failed in clean-up routine")	
	finally:	
		# Close Logging
		logging.debug("close Logging")	
		logging.info("socketServer exit()")
		logging.shutdown()
		ch.close()