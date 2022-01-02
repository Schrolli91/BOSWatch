#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
alarmMonitor

This is an alarmMonitor for receive alarm-messages from BOSWatch and show them on a touchscreen
The jsonSocketServer controlls an Watterott RPi-Display in case of received POCSAG-RIC

Implemented functions:
- show ric-description and alarm-message on display
- history of up to 5 alarms
- different colours for no alarm, test alarm and alarm
- playing a soundfile in case of an alarm
- show POCSAG is alive status (coloured clock)
- asynchronous threads for display control
- auto-turn-off display
- status informations
- rotating logfile in /var/log/alarmMonitor

@author: Jens Herrmann

BOSWatch:    https://github.com/Schrolli91/BOSWatch
RPi-Display: https://github.com/watterott/RPi-Display
"""

import logging
import logging.handlers
import configparser

import os
import time
import socket # for socket
import json # for data
from threading import Thread
import pygame

import globalData

try: 
	#
	# Logging
	#
	try:
		# set/create log_path
		log_path = "/var/log/alarmMonitor/"
		if not os.path.exists(log_path):
			os.mkdir(log_path)

		# init logger	
		myLogger = logging.getLogger()
		myLogger.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')

		# display logger
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO) 
		#ch.setLevel(logging.DEBUG) 
		ch.setFormatter(formatter)
		myLogger.addHandler(ch)		
		
		# fileLogger:
		fh = logging.handlers.TimedRotatingFileHandler(log_path+"alarmMonitor.log", "midnight", interval=1, backupCount=7)
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(formatter)
		myLogger.addHandler(fh)
		# start with a new logfile
		fh.doRollover()
	except:
		# we couldn't work without logging -> exit
		logging.critical("cannot initialise logging")
		logging.debug("cannot initialise logging", exc_info=True)
		exit(1)

	
	#
	# Read config.ini
	#
	try:
		logging.debug("reading config file")
		globalData.config = configparser.SafeConfigParser()
		globalData.config.read("config.ini")
		# if given loglevel is debug:
		logging.debug("- [AlarmMonitor]")
		for key,val in globalData.config.items("AlarmMonitor"):
			logging.debug("-- %s = %s", key, val)
		logging.debug("- [Display]")
		for key,val in globalData.config.items("Display"):
			logging.debug("-- %s = %s", key, val)
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
		globalData.screenBackground = pygame.Color(globalData.config.get("AlarmMonitor","colourGreen"))
		logging.debug("Start displayPainter-thread")
		Thread(target=displayPainter).start()
		logging.debug("start autoTurnOffDisplay-thread")
		Thread(target=autoTurnOffDisplay).start()
		logging.debug("start eventHandler-thread")
		Thread(target=eventHandler).start()
	except:
		# we couldn't work without helper threads -> exit
		logging.critical("cannot start service-Threads")
		logging.debug("cannot start service-Threads", exc_info=True)
		exit(1)

	#
	# start socket
	#
	logging.debug("Start socketServer")
	sock = socket.socket () # TCP
	sock.bind(("",globalData.config.getint("AlarmMonitor","socketPort")))
	sock.listen(5)
	logging.debug("socketServer runs")

	#
	# Build Lists out of config-entries
	#
	logging.debug("create lists")
	keepAliveRICs         = [int(x.strip()) for x in globalData.config.get("AlarmMonitor","keepAliveRICs").replace(";", ",").split(",")]
	logging.debug("-- keepAliveRICs: %s", keepAliveRICs)
	alarmRICs             = [int(x.strip()) for x in globalData.config.get("AlarmMonitor","alarmRICs").replace(";", ",").split(",")]
	logging.debug("-- alarmRICs: %s", alarmRICs)
	functionCharTestAlarm = [str(x.strip()) for x in globalData.config.get("AlarmMonitor","functionCharTestAlarm").replace(";", ",").split(",")]
	logging.debug("-- functionCharTestAlarm: %s", functionCharTestAlarm)
	functionCharAlarm     = [str(x.strip()) for x in globalData.config.get("AlarmMonitor","functionCharAlarm").replace(";", ",").split(",")]
	logging.debug("-- functionCharAlarm: %s", functionCharAlarm)
	
	#
	# try to read History from MySQL-DB
	#
	try:
		if globalData.config.getboolean("AlarmMonitor","loadHistory") == True:
			import mysql.connector

			for key,val in globalData.config.items("MySQL"):
				logging.debug("-- %s = %s", key, val)
			
			# Connect to DB
			logging.debug("connect to MySQL")
			connection = mysql.connector.connect(host = globalData.config.get("MySQL","dbserver"), user = globalData.config.get("MySQL","dbuser"), passwd = globalData.config.get("MySQL","dbpassword"), db = globalData.config.get("MySQL","database"), charset='utf8')
			cursor = connection.cursor()
			logging.debug("MySQL connected")

			# read countKeepAlive 
			# precondition: keepAliveRICs set
			if (len(keepAliveRICs) > 0):
				sql = "SELECT COUNT(*) FROM "+globalData.config.get("MySQL","tablePOC")+" WHERE ric IN ("+globalData.config.get("AlarmMonitor","keepAliveRICs")+")"
				cursor.execute(sql)
				result = int(cursor.fetchone()[0])
				if result > 0:
					globalData.countKeepAlive = result
				logging.debug("-- countKeepAlive: %s", globalData.countKeepAlive)

			# read countAlarm 
			# precondition: alarmRics and functionChar set
			if (len(alarmRICs) > 0) and (len(functionCharAlarm) > 0):
				sql = "SELECT COUNT(*) FROM "+globalData.config.get("MySQL","tablePOC")+" WHERE ric IN ("+globalData.config.get("AlarmMonitor","alarmRICs")+")"
				if len(functionCharAlarm) == 1:
					sql += " AND functionChar IN ('" + functionCharAlarm[0] + "')"
				elif len(functionCharAlarm) > 1:
					sql += " AND functionChar IN " + str(tuple(functionCharAlarm))
				cursor.execute(sql)
				result = int(cursor.fetchone()[0])
				if result > 0:
					globalData.countAlarm = result
				logging.debug("-- countAlarm: %s", globalData.countAlarm)

			# read countTestAlarm 
			# precondition: alarmRics and functionCharTestAlarm set
			if (len(alarmRICs) > 0) and (len(functionCharTestAlarm) > 0):
				sql = "SELECT COUNT(*) FROM "+globalData.config.get("MySQL","tablePOC")+" WHERE ric IN ("+globalData.config.get("AlarmMonitor","alarmRICs")+")"
				if len(functionCharTestAlarm) == 1:
					sql += " AND functionChar IN ('" + functionCharTestAlarm[0] + "')"
				elif len(functionCharTestAlarm) > 1:
					sql += " AND functionChar IN " + str(tuple(functionCharTestAlarm))
				cursor.execute(sql)
				result = int(cursor.fetchone()[0])
				if result > 0:
					globalData.countTestAlarm = result
				logging.debug("-- countTestAlarm: %s", globalData.countTestAlarm)

			# read the last 5 events in reverse order
			# precondition: alarmRics and (functionChar or functionCharTestAlarm) set
			if (len(alarmRICs) > 0) and ((len(functionCharAlarm) > 0) or (len(functionCharTestAlarm) > 0)):
				sql  = "SELECT UNIX_TIMESTAMP(time), ric, functionChar, msg, description FROM "+globalData.config.get("MySQL","tablePOC")
				sql += " WHERE ric IN ("+globalData.config.get("AlarmMonitor","alarmRICs")+")"
				functionChar = functionCharAlarm + functionCharTestAlarm
				if len(functionChar) == 1:
					sql += " AND functionChar IN ('" + functionChar[0] + "')"
				elif len(functionChar) > 1:
					sql += " AND functionChar IN " + str(tuple(functionChar))
				sql += " ORDER BY time DESC LIMIT 0,5"
				cursor.execute(sql)
				# reverse sort into history data
				for (timestamp, ric, functionChar, msg, description) in reversed(cursor.fetchall()):
					data = {}
					data['timestamp'] = timestamp
					data['ric'] = ric
					data['functionChar'] = functionChar
					data['msg'] = msg
					data['description'] = description
					globalData.alarmHistory.append(data)
				logging.debug("-- history data loaded: %s", len(globalData.alarmHistory))
						
			logging.info("history loaded from database")
		# if db is enabled
		pass
	except:
		# error, but we could work without history
		logging.error("cannot load history from MySQL")
		logging.debug("cannot load history from MySQL", exc_info=True)
		pass
	finally:
		try:
			cursor.close()
			connection.close()
			logging.debug("MySQL closed")
		except:
			pass

	#
	# initialise alarm sound
	#
	alarmSound = False
	try:
		if globalData.config.getboolean("AlarmMonitor","playSound") == True:
			if not globalData.config.get("AlarmMonitor","soundFile") == "":
				pygame.mixer.init()
				alarmSound = pygame.mixer.Sound(globalData.config.get("AlarmMonitor","soundFile"))
				logging.info("alarm with sound")
	except:
		# error, but we could work without sound
		logging.error("cannot initialise alarm sound")
		logging.debug("cannot initialise alarm sound", exc_info=True)
		pass
				
	globalData.startTime = int(time.time())
	logging.info("alarmMonitor started - on standby")
		
	#
	# Main Program
	# (Threads will set abort to True if an error occurs)
	#
	while globalData.abort == False:
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
				
				# current time for this loop:
				curtime = int(time.time())

				# keep alive calculation with additional RICs
				if int(parsed_json['ric']) in keepAliveRICs:
					logging.info("POCSAG is alive")
					globalData.lastAlarm = curtime
					globalData.countKeepAlive += 1

				# (test) alarm processing
				elif int(parsed_json['ric']) in alarmRICs:
					if parsed_json['functionChar'] in functionCharTestAlarm:
						logging.info("--> Probealarm: %s", parsed_json['ric'])
						globalData.screenBackground = pygame.Color(globalData.config.get("AlarmMonitor","colourYellow"))
						globalData.countTestAlarm += 1
					elif parsed_json['functionChar'] in functionCharAlarm:
						logging.info("--> Alarm: %s", parsed_json['ric'])
						globalData.screenBackground = pygame.Color(globalData.config.get("AlarmMonitor","colourRed"))
						globalData.countAlarm += 1
						
					# forward data to alarmMonitor
					globalData.data = parsed_json
					globalData.data['timestamp'] = curtime
					logging.debug("-- data: %s", parsed_json)
					# save 5 alarm history entries
					globalData.alarmHistory.append(globalData.data)
					if len(globalData.alarmHistory) > 5:
						globalData.alarmHistory.pop(0)
					# update lastAlarm for keep alive calculation
					globalData.lastAlarm = curtime
					# enable display for n seconds:
					globalData.enableDisplayUntil = curtime + globalData.config.getint("AlarmMonitor","showAlarmTime")
					# tell alarm-thread to turn on the display
					globalData.navigation = "alarmPage"
					globalData.showDisplay = True;
					
					# play alarmSound...
					if not alarmSound == False:
						# ... but only one per time...
						if pygame.mixer.get_busy() == False:
							alarmSound.play()
							logging.debug("sound started")
					
			except KeyError:
				# we will ignore waste in json_string
				logging.warning("No RIC found: %s", json_string)
				pass
	
except KeyboardInterrupt:
	logging.warning("Keyboard Interrupt")	
	exit(0)	
except SystemExit:
	logging.warning("SystemExit received")
	exit(0)
except:
	logging.exception("unknown error")
finally:
	try:
		logging.info("socketServer shuting down")
		globalData.running = False
		sock.close()
		logging.debug("socket closed") 
		if not alarmSound == False:
			pygame.mixer.quit()
			logging.debug("mixer closed") 
		if connection:
			connection.close()
			logging.debug("MySQL closed") 
		time.sleep(0.5)
		logging.debug("exiting socketServer")		
	except:
		logging.warning("failed in clean-up routine")	
	finally:	
		# Close Logging
		logging.debug("close Logging")	
		logging.info("socketServer exit()")
		logging.shutdown()
		ch.close()