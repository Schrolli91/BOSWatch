#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Plugin for calling FHEM home automation

@author: Marco Schotthöfer

@requires: python-fhem (pip install fhem)
"""

#
# Imports
#
import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
#from includes.helper import timeHandler
#from includes.helper import wildcardHandler
from includes.helper import configHandler
from includes.helper import wildcardHandler
import fhem

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
		if configHandler.checkConfig("fhemCmd"): #read and debug the config (let empty if no config used)

			protocol = globalVars.config.get("fhemCmd", "protocol")
			logging.debug("protocol: %s", protocol)
			
			server = globalVars.config.get("fhemCmd", "server")
			logging.debug("server: %s", server)
			
			port = globalVars.config.get("fhemCmd", "port")
			logging.debug("port: %s", port)
			
			username = globalVars.config.get("fhemCmd", "username")
			logging.debug("username: %s", username)
			
			password = globalVars.config.get("fhemCmd", "password")
			logging.debug("password: %s", password)
			
			########## User Plugin CODE ##########
			fh = fhem.Fhem(server=server, protocol=protocol, port=port, username=username, password=password)
			
			if typ == "FMS":
				fhemCommand = globalVars.config.get("fhemCmd", "commandFMS")
			elif typ == "ZVEI":
				fhemCommand = globalVars.config.get("fhemCmd", "commandZVEI")
			elif typ == "POC":
				fhemCommand = globalVars.config.get("fhemCmd", "commandPOC")
			else:
				logging.warning("Invalid Typ: %s", typ)
				return False
			
			fhemCommand = wildcardHandler.replaceWildcards(fhemCommand, data)
			logging.debug("fhemCommand: %s", fhemCommand)
                        
			fh.send_cmd(fhemCommand)
			del fh
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
