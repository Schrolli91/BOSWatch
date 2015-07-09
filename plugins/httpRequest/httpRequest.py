#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
httpRequest-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages to an URL

@author: Bastian Schroll

@requires: httpRequest-Configuration has to be set in the config.ini
"""

import time
import logging # Global logger
import httplib #for the HTTP request
from urlparse import urlparse #for split the URL into url and path

from includes import globals  # Global variables

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
	"""
	# nothing to do for this plugin
	return


##
#
# Main function of HTTP-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the httpRequest-Plugin.
	It will send the data to an URL via http Request

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  httpRequest-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("httpRequest"): #read and debug the config

			try:
				#
				# Create URL
				#
				if typ == "FMS":
					url = globals.config.get("httpRequest", "fms_url") #Get URL
					url = wildcardHandler.replaceWildcards(url, data) # replace wildcards with helper function
				elif typ == "ZVEI":
					url = globals.config.get("httpRequest", "zvei_url") #Get URL
					url = wildcardHandler.replaceWildcards(url, data) # replace wildcards with helper function
				elif typ == "POC":
					url = globals.config.get("httpRequest", "poc_url") #Get URL
					url = wildcardHandler.replaceWildcards(url, data) # replace wildcards with helper function

				else:
					logging.warning("Invalid Typ: %s", typ)
					return


				#
				# HTTP-Request
				#
				logging.debug("send %s HTTP request", typ)
				url = urlparse(url) #split URL into path and querry
				httprequest = httplib.HTTPConnection(url[2]) #connect to URL Path
				httprequest.request("GET", url[5]) #send URL Querry per GET

			except:
				logging.error("cannot send HTTP request")
				logging.debug("cannot send HTTP request", exc_info=True)
				return

			else:
				try:
					#
					# check HTTP-Response
					#
					httpresponse = httprequest.getresponse()
					if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
						logging.debug("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
					else:
						logging.warning("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
				except: #otherwise
					logging.error("cannot get HTTP response")
					logging.debug("cannot get HTTP response", exc_info=True)
					return

			finally:
				logging.debug("close HTTP-Connection")
				try:
					httprequest.close()
				except:
					pass

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
