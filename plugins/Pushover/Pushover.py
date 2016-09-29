#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Pushover-Plugin to send FMS-, ZVEI- and POCSAG - messages to Pushover Clients

@author: Ricardo Krippner

@requires: Pushover-Configuration has to be set in the config.ini
"""

import time
import logging # Global logger
import httplib #for the HTTP request
import urllib
from includes import globals  # Global variables

from includes.helper import timeHandler
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
	"""
	# nothing to do for this plugin
	return


##
#
# Main function of Pushover-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the Pushover-Plugin.
	It will send the data to Pushover API

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  Pushover-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("Pushover"): #read and debug the config

			try:
				#
				# Pushover-Request
				#
				logging.debug("send Pushover %s", typ)

			        if data["function"] == '1':
			                priority = globals.config.get("Pushover", "SubA")
			        elif data["function"] == '2':
			                priority = globals.config.get("Pushover", "SubB")
			        elif data["function"] == '3':
			                priority = globals.config.get("Pushover", "SubC")
			        elif data["function"] == '4':
			                priority = globals.config.get("Pushover", "SubD")
			        else:
			                priority = 0

				conn = httplib.HTTPSConnection("api.pushover.net:443")
				conn.request("POST", "/1/messages.json",
				urllib.urlencode({
					"token": globals.config.get("Pushover", "api_key"),
					"user": globals.config.get("Pushover", "user_key"),
					"message": "<b>"+data["description"]+"</b><br>"+data["msg"].replace(";", "<br>"),
					"html": globals.config.get("Pushover", "html"),
					"title": globals.config.get("Pushover", "title"),
					"priority": priority,
					"retry": globals.config.get("Pushover", "retry"),
					"expire": globals.config.get("Pushover", "expire")
				}),{"Content-type": "application/x-www-form-urlencoded"})

			except:
				logging.error("cannot send Pushover request")
				logging.debug("cannot send Pushover request", exc_info=True)
				return

			else:
				try:
					#
					# check Pushover-Response
					#
					response = conn.getresponse()
					if str(response.status) == "200": #Check Pushover Response and print a Log or Error
						logging.debug("Pushover response: %s - %s" , str(response.status), str(response.reason))
					else:
						logging.warning("Pushover response: %s - %s" , str(response.status), str(response.reason))
				except: #otherwise
					logging.error("cannot get Pushover response")
					logging.debug("cannot get Pushover response", exc_info=True)
					return

			finally:
				logging.debug("close Pushover-Connection")
				try:
					request.close()
				except:
					pass

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
