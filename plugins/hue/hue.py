#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

Plugin to control Philips hue lights and switches

@author: Fabian Kessler

@requires: none
"""

#
# Imports
#
import logging # Global logger
from includes import globalVars  # Global variables
import json
import requests
import time

# Helper function, uncomment to use
#from includes.helper import timeHandler
#from includes.helper import wildcardHandler
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
	try:
		########## User onLoad CODE ##########
		pass
		########## User onLoad CODE ##########
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
		raise

##
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the Plugin.
	If necessary the configuration hast to be set in the config.ini.
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
		if configHandler.checkConfig("hue"): #read and debug the config
			#for debugging
			"""logging.debug(globalVars.config.get("hue", "bridgeip"))
			logging.debug(globalVars.config.get("hue", "deviceid"))
			logging.debug(globalVars.config.get("hue", "apikey"))
			logging.debug(globalVars.config.getint("hue", "repeat"))
			logging.debug(globalVars.config.getint("hue", "timeon"))
			logging.debug(globalVars.config.getint("hue", "timeoff"))
			logging.debug(globalVars.config.getint("hue", "keepon"))"""

			########## User Plugin CODE ##########
			if typ == "FMS":
				logging.warning("%s not supported", typ)
			elif typ == "ZVEI":
				logging.warning("%s not supported", typ)
			elif typ == "POC":
				#logging.warning("%s not supported", typ)
				logging.debug("POC received")
				bridgeip = globalVars.config.get("hue", "bridgeip")
				deviceid = globalVars.config.get("hue", "deviceid")
				apikey = globalVars.config.get("hue", "apikey")
				repeat = globalVars.config.getint("hue", "repeat")
				timeon = globalVars.config.getint("hue", "timeon")
				timeoff = globalVars.config.getint("hue", "timeoff")
				keepon = globalVars.config.getint("hue", "keepon")
				data_on = '{"on":true}'
				data_off = '{"on":false}'
				url = "http://" + bridgeip + "/api/" + apikey + "/lights/" + deviceid + "/state"
				logging.debug("hue REST API URL: %s", url)
				
				#blinking  
				for _ in range(repeat):
					requests.put(url, data=data_on)
					logging.debug("on for %s seconds", timeon)
					time.sleep(timeon)
					requests.put(url, data=data_off)
					logging.debug("off for %s seconds", timeoff)
					time.sleep(timeoff)
				if keepon > 0:
					logging.debug("switch to on and wait for keepon to expire")
					requests.put(url, data=data_on)
					logging.debug("keep on for %s seconds", keepon)
					time.sleep(keepon)
					requests.put(url, data=data_off)
				else:
					logging.debug("switch to on and exit plugin")
					requests.put(url, data=data_on)
			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
