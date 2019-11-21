#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

	"""
	global GPIOPIN
	global waitTime
    
	GPIOPIN = globalVars.config.getint("gpiocontrol","pin")
	waitTime = globalVars.config.getint("gpiocontrol","triggertime")
    

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(GPIOPIN, GPIO.OUT)
  	GPIO.output(GPIOPIN, GPIO.HIGH)

	return

#
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	try:
		if configHandler.checkConfig("gpiocontrol"): #read and debug the config

			logging.debug(globalVars.config.get("gpiocontrol", "pin"))
			logging.debug(globalVars.config.get("gpiocontrol", "triggertime"))
   			logging.debug(globalVars.config.get("gpiocontrol", "activerics"))
            
			########## User Plugin CODE ##########
			if typ == "FMS":
				logging.warning("%s not supported", typ)
			elif typ == "ZVEI":
				logging.warning("%s not supported", typ)
			elif typ == "POC":
                if globalVars.config.get("gpiocontrol", "activerics") == "":
                    th = threading.Thread(target = trigger)
                    th.start()
                else
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
	logging.info("GPIOPIN %s on", GPIOPIN)
	time.sleep(waitTime)
  	GPIO.output(GPIOPIN, GPIO.HIGH)
	logging.info("GPIOPIN %s off", GPIOPIN)

	return
