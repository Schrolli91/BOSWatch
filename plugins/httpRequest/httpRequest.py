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
from includes import helper #Global helper functions

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
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("httpRequest"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.error("cannot read config file")
			logging.debug("cannot read config file", exc_info=True)
		else: # Without config, plugin couldn't work

			try:
				#
				# Create URL
				#
				logging.debug("send %s HTTP request", typ)

				if typ == "FMS":
					url = globals.config.get("httpRequest", "fms_url") #Get URL
					url = url.replace("%FMS%", data["fms"]).replace("%STATUS%", data["status"]) #replace Wildcards
					url = url.replace("%DIR%", data["direction"]).replace("%DIRT%", data["directionText"]) #replace Wildcards
					url = url.replace("%TSI%", data["tsi"]) #replace Wildcards
				elif typ == "ZVEI":
					url = globals.config.get("httpRequest", "zvei_url") #Get URL
					url = url.replace("%ZVEI%", data["zvei"]) #replace Wildcards
				elif typ == "POC":
					url = globals.config.get("httpRequest", "poc_url") #Get URL
					url = url.replace("%RIC%", data["ric"]) #replace Wildcards
					url = url.replace("%FUNC%", data["function"]).replace("%FUNCCHAR%", data["functionChar"]) #replace Wildcards
					url = url.replace("%MSG%", data["msg"]).replace("%BITRATE%", str(data["bitrate"])) #replace Wildcards
				else:
					logging.warning("Invalid Typ: %s", typ)
					return

				#same in all types
				url = url.replace("%DESCR%", data["description"]) # replace Wildcards
				url = url.replace("%TIME%", helper.curtime("%H:%M:%S")) # replace Wildcards
				url = url.replace("%DATE%", helper.curtime("%d.%m.%Y")) # replace Wildcards

				#
				# HTTP-Request
				#
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
