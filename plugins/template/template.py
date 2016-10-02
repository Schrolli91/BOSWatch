#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
template plugin to show the function and usage of plugins
feel free to edit to yout own plugin
please edit theese desciption, the @author-Tag and the @requires-Tag
For more information take a look into the other plugins

@author: Jens Herrmann
@author: Bastian Schroll

@requires: none
"""

#
# Imports
#
import logging # Global logger
from includes import globals  # Global variables

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
		if configHandler.checkConfig("template"): #read and debug the config (let empty if no config used)

			########## User Plugin CODE ##########
			if typ == "FMS":
				logging.warning("%s not supported", typ)
			elif typ == "ZVEI":
				logging.warning("%s not supported", typ)
			elif typ == "POC":
				logging.warning("%s not supported", typ)
			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
