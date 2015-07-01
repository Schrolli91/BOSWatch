#!/usr/bin/python
# -*- coding: cp1252 -*-

###########################################################################
# Use this as a simple Plugin Loading Tool to test your own Coded Plugins #
###########################################################################

import logging

import ConfigParser #for parse the config file
import os #for log mkdir
import time #timestamp for doublealarm

from includes import globals  # Global variables
from includes import pluginLoader
from includes import alarmHandler
from includes import filter

#create new logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#set log string format
formatter = logging.Formatter('%(asctime)s - %(module)-15s %(funcName)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')

#create a display loger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG) #log level >= info
ch.setFormatter(formatter)
logger.addHandler(ch)

#https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
#log levels
#----------
#debug - debug messages only for log
#info - information for normal display
#warning
#error - normal error - program goes further
#exception - error with exception message in log
#critical - critical error, program exit

globals.script_path = os.path.dirname(os.path.abspath(__file__))

try:
	logging.debug("reading config file")
	globals.config = ConfigParser.ConfigParser()
	globals.config.read(globals.script_path+"/config/config.ini")
	for key,val in globals.config.items("Plugins"):
		logging.debug(" - %s = %s", key, val)	
except:
	logging.exception("cannot read config file")


pluginLoader.loadPlugins()		

filter.loadFilters()


# ----- Test Data ----- #
#typ = "FMS"
#data = {"fms":"12345678", "status":"2", "direction":"1", "tsi":"III"}

typ = "ZVEI"
data = {"zvei":"25345"}

#typ = "POC"
#data = {"ric":"1234567", "function":"1", "msg":"Hello World!, "bitrate":"1200"}
	
while True:
	try:
		time.sleep(1)
		
		print ""
		alarmHandler.processAlarm(typ,"0",data)
		
	except KeyboardInterrupt:
		logging.warning("Keyboard Interrupt")	
		exit()
	except:
		logging.exception("unknown error")
		exit()
