#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
firEmergency-Plugin to dispatch ZVEI- and POCSAG - messages to firEmergency

firEmergency configuration:
- set input to "FMS32" at Port 5555

@autor: Smith-fms

@requires: firEmergency-Configuration has to be set in the config.ini
"""

import logging # Global logger
import socket

from includes import globalVars  # Global variables

from includes.helper import configHandler
from includes.helper import stringConverter


###
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
# Main function of firEmergency-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the firEmergency-Plugin.
	It will send the data to an firEmergency-Instance.

	The configuration for the firEmergency-Connection is set in the config.ini.

	@type    typ:  string (ZVEI|POC)
	@param   typ:  Typ of the dataset for sending to firEmergency
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch to firEmergency.
	@type    freq: string
	@keyword freq: frequency is not used in this plugin

	@requires:  firEmergency-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("firEmergency"): #read and debug the config

			try:
				#
				# connect to firEmergency
				#
				firSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				firSocket.connect((globals.config.get("firEmergency", "firserver"), globals.config.getint("firEmergency", "firport")))
			except:
				logging.error("cannot connect to firEmergency")
				logging.debug("cannot connect to firEmergency", exc_info=True)
				# Without connection, plugin couldn't work
				return

			else:
				#
				# Format given data-structure to xml-string for firEmergency
				#
				if typ == "FMS":
					logging.debug("FMS not supported by firEmgency")

				elif typ == "ZVEI":
					logging.debug("ZVEI to firEmergency")
					try:
							description = stringConverter.convertToUTF8(data["description"])
							firXML = "<event>\n<address>"+data["zvei"]+"</address>\n<description>"+description+"</description>\n<message>"+data["zvei"]+"</message>\n</event>\n"
							firSocket.send(firXML)
					except:
							logging.error("%s to firEmergency failed", typ)
							logging.debug("%s to firEmergency failed", typ, exc_info=True)
							# Without connection, plugin couldn't work
							return

				elif typ == "POC":
					logging.debug("POC to firEmergency")
					try:
							# !!! Subric+"XX" because of an Issuse in firEmergency !!!
							description = stringConverter.convertToUTF8(data["description"])
							msg =  stringConverter.convertToUTF8(data["msg"])
							firXML = "<event>\n<address>"+data["ric"]+"</address>\n<status>"+data["function"]+"XX</status>\n<description>"+description+"</description>\n<message>"+msg+"</message>\n</event>\n"
							firSocket.send(firXML)
					except:
							logging.error("%s to firEmergency failed", typ)
							logging.debug("%s to firEmergency failed", typ, exc_info=True)
							# Without connection, plugin couldn't work
							return

				else:
					logging.warning("Invalid Typ: %s", typ)

			finally:
				logging.debug("close firEmergency-Connection")
				try:
					firSocket.close()
				except:
					pass

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
