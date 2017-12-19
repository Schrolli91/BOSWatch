#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
httpRequest-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages to an URL

@author: Bastian Schroll
@author: TheJockel


@requires: httpRequest-Configuration has to be set in the config.ini
"""

#
# Imports
#
import urllib
import urllib2
import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
#from includes.helper import timeHandler
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
	@type    data: map of data (structure see readme.md in plugin folder)
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
				# Make a copy of the data field to not overwrite the data in it
				# Replace special characters in dataCopy Strings for URL
				#
				dataCopy = data
				for key in dataCopy:
					if isinstance(dataCopy[key], basestring):
						dataCopy[key] = urllib.quote(dataCopy[key])
				#
				# Get URLs
				#
				if typ == "FMS":
					urls = globalVars.config.get("httpRequest", "fms_url").split(",")
				elif typ == "ZVEI":
					urls = globalVars.config.get("httpRequest", "zvei_url").split(",")
				elif typ == "POC":
					urls = globalVars.config.get("httpRequest", "poc_url").split(",")
				else:
					logging.warning("Invalid Typ: %s", typ)
					return

				#
				# replace wildcards
				#
				for (i, url) in enumerate(urls):
					urls[i] = wildcardHandler.replaceWildcards(urls[i].strip(), dataCopy)
				#
				# HTTP-Request
				#
				logging.debug("send %s HTTP requests", typ)

				for url in urls:
					try:
						urllib2.urlopen(url)
					except urllib2.HTTPError as e:
    						logging.warning("HTTP response: %s", e.code)
					except urllib2.URLError as e:
    						logging.warning("HTTP-specific error: %s", e.args)

			except:
				logging.error("cannot send HTTP request")
				logging.debug("cannot send HTTP request", exc_info=True)
				return
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
