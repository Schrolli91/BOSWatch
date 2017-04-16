#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
SMS77-Plugin to send FMS-, ZVEI- and POCSAG - messages to SMS77

@author: Ricardo Krippner

@requires: SMS77-Configuration has to be set in the config.ini
"""

import logging # Global logger
import httplib #for the HTTP request
import urllib
from includes import globalVars  # Global variables

#from includes.helper import timeHandler
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
# Main function of SMS77-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the Sms77-Plugin.
	It will send the data to Sms77 API

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  Sms77-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("Sms77"): #read and debug the config
			
			# create an empty message an fill it with the required information
			message = ""
			if typ == "FMS":
				logging.debug("FMS detected, building message")
				message = data["description"]+"<br>"+data["status"]
			elif typ == "ZVEI":
				logging.debug("ZVEI detected, building message")
				mesage = data["description"]
			elif typ == "POC":
				logging.debug("POC detected, building message")
				message = data["description"]+"<br>"+data["msg"].replace(";", "<br>")
			else:
				logging.warning("Invalid typ - use empty message")

			try:

				#
				# Sms77-Request
				#
				logging.debug("send Sms77 %s", typ)

				conn = httplib.HTTPSConnection("gateway.sms77.de:443")
				conn.request("POST", "",
				urllib.urlencode({
					"u": globalVars.config.get("Sms77", "user"),
					"p": globalVars.config.get("Sms77", "password"),
					"to": globalVars.config.get("Sms77", "to"),
					"from": globalVars.config.get("Sms77", "from"),
					"type": globalVars.config.get("Sms77", "type"),
					"text": message
				}),{"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"})

			except:
				logging.error("cannot send SMS77 request")
				logging.debug("cannot send SMS77 request", exc_info=True)
				return

			else:
				try:
					#
					# check Sms77-Response
					#
					response = conn.getresponse()
					if str(response.status) == "200": #Check Sms77 Response and print a Log or Error
						logging.debug("SMS77 response: %s - %s" , str(response.status), str(response.reason))
					else:
						logging.warning("SMS77 response: %s - %s" , str(response.status), str(response.reason))
				except: #otherwise
					logging.error("cannot get SMS77 response")
					logging.debug("cannot get SMS77 response", exc_info=True)
					return

			finally:
				logging.debug("close Sms77-Connection")
				try:
					request.close()
				except:
					pass

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
