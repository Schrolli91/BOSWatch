#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
notifyMyAndroid-Plugin to dispatch FMS-, ZVEI- and POCSAG-messages via UDP/TCP

@author: Jens Herrmann

@requires: notifyMyAndroid-Configuration has to be set in the config.ini
"""

import logging # Global logger

import socket  # for connection
import json    # for data-transfer

from includes import globals  # Global variables

from includes.helper import configHandler
from includes.helper import timeHandler
from includes.helper import uft8Converter  # UTF-8 converter
from includes.pynma import pynma

# local variables
application = "BOSWatch"
APIKey = None

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
	# local variables
	global application
	global APIKey
	
	# load config:
	configHandler.checkConfig("notifyMyAndroid")
	APIKey = globals.config.get("notifyMyAndroid","APIKey")
	application = globals.config.get("notifyMyAndroid","appName")

	return


##
#
# Main function of jsonSocket-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the notifyMyAndroid-Plugin.
	
	The configuration is set in the config.ini.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending via UDP/TCP
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to UDP.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  notifyMyAndroid-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	# local variables
	global application
	global APIKey
	
	try:
		try:
			#
			# initialize to pyNMA
			#
			nma = pynma.PyNMA(APIKey)

		except:
			logging.error("cannot initialize pyNMA")
			logging.debug("cannot initialize %s-socket", exc_info=True)
			# Without class, plugin couldn't work
			return

		else:
			# toDo is equals for all types, so only check if typ is supported
			supportedTypes = ["FMS", "ZVEI", "POC"]
			if typ in supportedTypes:
				logging.debug("Start %s to NMA", typ)
				try:
					# send data
					event = data['description']
					msg   = timeHandler.curtime() 
					if len(data['msg']) > 0:
						msg += "\n" + data['msg']
					response = nma.push(application, uft8Converter.convertToUTF8(event), uft8Converter.convertToUTF8(msg), priority=globals.config.getint("notifyMyAndroid","priority"))
				except:
					logging.error("%s to NMA failed", typ)
					logging.debug("%s to NMA failed", typ, exc_info=True)
					return
				else:
					try:
						#
						# check HTTP-Response
						#
						if str(response[APIKey]['code']) == "200": #Check HTTP Response an print a Log or Error
							logging.debug("NMA response: %s" , str(response[APIKey]['code']))
							if int(response[APIKey]['remaining']) == 0:
								logging.error("NMA remaining msgs: %s" , str(response[APIKey]['remaining']))
							if int(response[APIKey]['remaining']) < 20:
								logging.warning("NMA remaining msgs: %s" , str(response[APIKey]['remaining']))
							else:
								logging.debug("NMA remaining msgs: %s" , str(response[APIKey]['remaining']))
						else:
							logging.warning("NMA response: %s - %s" , str(response[APIKey]['code']), str(response[APIKey]['message']))
					except: #otherwise
						logging.error("cannot read pynma response")
						logging.debug("cannot read pynma response", exc_info=True)
						return						
			else:
				logging.warning("Invalid Typ: %s", typ)

	except:
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
