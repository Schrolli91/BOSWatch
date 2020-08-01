#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

@author: KS

@requires: none
"""

# Imports

import RPi.GPIO as GPIO
import time
import threading

import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
from includes.helper import timeHandler
from includes.helper import wildcardHandler
from includes.helper import configHandler

##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine is called one time for initialize the plugin

	@requires:  nothing

	@return:    nothing
	@exception: Exception if init has an fatal error so that the plugin couldn't work

	"""
	global GPIOPIN
	global waitTime

	GPIOPIN = globalVars.config.getint("gpiocontrol","pin")
	waitTime = globalVars.config.getint("gpiocontrol","triggertime")

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(GPIOPIN, GPIO.OUT)

	#GPIO schalten beim START
    	#GPIO.output(GPIOPIN, GPIO.LOW)
	#time.sleep(1)

	GPIO.output(GPIOPIN, GPIO.HIGH)

	return

#
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  If necessary the configuration hast to be set in the config.ini.

	@return:    nothing
	@exception: nothing, make sure this function will never thrown an exception
	"""
	try:
		if configHandler.checkConfig("gpiocontrol"): #read and debug the config (let empty if no config used)

			logging.debug(globalVars.config.get("gpiocontrol", "pin"))
			logging.debug(globalVars.config.get("gpiocontrol", "triggertime"))

			########## User Plugin CODE ##########
			if typ == "FMS":
				th = threading.Thread(target = trigger)
				th.start()
				#logging.warning("%s not supported", typ)
			elif typ == "ZVEI":
				th = threading.Thread(target = trigger)
				th.start()
				#logging.warning("%s not supported", typ)
			elif typ == "POC":
				if globalVars.config.get("gpiocontrol", "activerics") == "":
					th = threading.Thread(target = trigger)
					th.start()
				else:
					if  data["ric"] in globalVars.config.get("gpiocontrol", "activerics"):
						th = threading.Thread(target = trigger)
						th.start()
					else:
						logging.info("Ric not in activerics")
			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)

def trigger():
	GPIO.output(GPIOPIN, GPIO.LOW)
	logging.info("GPIOPIN %s angeschaltet", GPIOPIN)
	time.sleep(waitTime)
        GPIO.output(GPIOPIN, GPIO.HIGH)
	logging.info("GPIOPIN %s ausgeschaltet", GPIOPIN)

	return
