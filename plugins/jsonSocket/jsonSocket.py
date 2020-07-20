#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
jsonSocket-Plugin to dispatch FMS-, ZVEI- and POCSAG-messages via UDP/TCP

@author: Jens Herrmann

@requires: jsonSocket-Configuration has to be set in the config.ini
"""

import logging # Global logger

import socket  # for connection
import json    # for data-transfer

from includes import globalVars  # Global variables

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
# Main function of jsonSocket-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the jsonSocket-Plugin.
	It will send the data via UDP/TCP

	The configuration for the Connection is set in the config.ini.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending via UDP/TCP
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch to UDP.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  jsonSocket-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("jsonSocket"): #read and debug the config

			try:
					#
				# initialize to socket-Server
				#
				# SOCK_DGRAM is the socket type to use for UDP sockets
				# SOCK_STREAM is the socket type to use for TCP sockets
				if globalVars.config.get("jsonSocket", "protocol") == "TCP":
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect((globalVars.config.get("jsonSocket", "server"), globalVars.config.getint("jsonSocket", "port")))
				else:
					sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			except:
				logging.error("cannot initialize %s-socket", globalVars.config.get("jsonSocket", "protocol"))
				logging.debug("cannot initialize %s-socket", globalVars.config.get("jsonSocket", "protocol"), exc_info=True)
				# Without connection, plugin couldn't work
				return

			else:
				# toDo is equals for all types, so only check if typ is supported
				supportedTypes = ["FMS", "ZVEI", "POC"]
				if typ in supportedTypes:
					logging.debug("Start %s to %s", typ, globalVars.config.get("jsonSocket", "protocol"))
					try:
						# dump data to json-string
						sendData = json.dumps(data)
						# send data
						sock.sendto(sendData, (globalVars.config.get("jsonSocket", "server"), globalVars.config.getint("jsonSocket", "port")))
					except:
						logging.error("%s to %s failed", typ, globalVars.config.get("jsonSocket", "protocol"))
						logging.debug("%s to %s failed", typ, globalVars.config.get("jsonSocket", "protocol"), exc_info=True)
						return

				else:
					logging.warning("Invalid Typ: %s", typ)

			finally:
				logging.debug("close %s-Connection", globalVars.config.get("jsonSocket", "protocol"))
				try:
					sock.close()
				except:
					pass

	except:
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
