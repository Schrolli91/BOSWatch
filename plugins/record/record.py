#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""

@author: DK5RA Alex(trollkopp)

@requires: arecord >= 1.1.3 
"""

# ADD THIS TO YOUR Pulseaudio config file /etc/pulse/default.pa
# load-module module-null-sink sink_name=playbackstream
# update-sink-proplist playbackstream device.description=playbackstream
# load-module module-loopback sink=playbackstream
# set-default-sink playbackstream
# set-default-source playbackstream.monitor


#
# Imports
#

import logging # Global logger
from includes import globalVars  # Global variables


import os           # for log mkdir
import time         # for time.sleep()
import subprocess   # for starting record

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
		if configHandler.checkConfig("record"): #read and debug the config (let empty if no config used)

			logging.debug(globalVars.config.get("Plugins", "record"))
#			logging.debug(globalVars.config.get("template", "test2"))
			rec_duration = globalVars.config.get("record", "rec_duration")
			if (globalVars.config.get("Plugins", "record") == "1"):
				########## User Plugin CODE ##########
				if typ == "FMS":
					logging.warning("%s not supported", typ)
				elif typ == "ZVEI":
					logging.debug("record plugin: detected ZVEI decode")
					timestamp = str(timeHandler.getDate())+"-"+str(timeHandler.getTime())
					zveicode = "%ZVEI%"
					zveicode = wildcardHandler.replaceWildcards(zveicode, data)
					filename = "aufnahme_"+"5-ton"+str(zveicode)+"_"+str(timestamp)+".wav"
					rec_filepath = globalVars.config.get("record", "filepath")
					logging.debug(filename)
					logging.debug(rec_filepath)
					command = ""
					command = command+"arecord -D pulse -f cd -d "+str(rec_duration)+" -c 1 "+str(rec_filepath)+str(filename)+""
					recordstream = subprocess.Popen(command.split(),
					stderr=open(globalVars.log_path+"record.log","a"),
					shell=False)
				elif typ == "POC":
					logging.warning("%s not supported", typ)
				else:
					logging.warning("Invalid Typ: %s", typ)
				########## User Plugin CODE ##########
			else:
				logging.debug("record plugin not activated. activate it in the config.ini")
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
