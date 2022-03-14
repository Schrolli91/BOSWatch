#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: KS

@requires: paho-mqtt
"""

#
# Imports
#
import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
from includes.helper import timeHandler
from includes.helper import wildcardHandler
from includes.helper import configHandler

import paho.mqtt.client as mqtt
import json

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
		if configHandler.checkConfig("mqtt"): #read and debug the config (let empty if no config used)

			logging.debug(globalVars.config.get("mqtt", "brokeraddress"))
			logging.debug(globalVars.config.get("mqtt", "topic"))
			########## User Plugin CODE ##########
			broker_address = globalVars.config.get("mqtt", "brokeraddress")
			topic = globalVars.config.get("mqtt", "topic")

            broker_username = globalVars.config.get("mqtt", "brokerusername")
            broker_password = globalVars.config.get("mqtt", "brokerpassword")

            mqttClient = mqtt.Client()

			if typ == "FMS":
				x = {
					"fms": data["fms"],
					"status": data["status"],
					"direction": data["direction"],
					"directionText": data["directionText"],
					"tsi": data["tsi"],
					"description": data["description"],
					"timestamp": timeHandler.curtime()
				}
			elif typ == "ZVEI":
				x = {
					"zvei": data["zvei"],
					"description": data["description"],
					"timestamp": timeHandler.curtime()
				}
			elif typ == "POC":
				functionText = "%FUNCTEXT%"
				functionText = wildcardHandler.replaceWildcards(functionText, data)
				x = {
					"ric": data["ric"],
					"function": data["function"],
					"functionText": functionText,
					"functionChar": data["functionChar"],
					"msg": data["msg"],
					"bitrate": data["bitrate"],
					"description": data["description"],
					"timestamp": timeHandler.curtime()
				}
			else:
				logging.warning("Invalid Typ: %s", typ)
			
			y = json.dumps(x)


            ## only login if there is a username given
            if( len(broker_username) > 0 ):
                mqttClient.username_pw_set(broker_username, broker_password)

			mqttClient.connect(broker_address)
			mqttClient.publish(topic,y)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
