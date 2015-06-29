#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
jsonSocket-Plugin to dispatch FMS-, ZVEI- and POCSAG-messages via UDP/TCP

@author: Jens Herrmann

@requires: jsonSocket-Configuration has to be set in the config.ini
"""

import logging # Global logger

import socket  # for connection
import json    # for data-transfer

from includes import globals  # Global variables

##
#
# onLoad function of plugin
# will be called by the pluginLoader
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine are called

	@requires:  nothing
	
	@return:    nothing
	"""
	try:
		########## User onLoad CODE ##########
		
		########## User onLoad CODE ##########
		
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)

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
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to UDP.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  jsonSocket-Configuration has to be set in the config.ini
	
	@return:    nothing
	"""
	try:
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("jsonSocket"):
				logging.debug(" - %s = %s", key, val)
				
		except:
			logging.error("cannot read config file")
			logging.debug("cannot read config file", exc_info=True)
		else: # Without config, plugin couldn't work

			try:
					#
				# initialize to socket-Server
				#
				# SOCK_DGRAM is the socket type to use for UDP sockets
				# SOCK_STREAM is the socket type to use for TCP sockets
				if globals.config.get("jsonSocket", "protocol") == "TCP":
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect((globals.config.get("jsonSocket", "server"), globals.config.getint("jsonSocket", "port")))
				else:
					sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				
			except:
				logging.error("cannot initialize %s-socket", globals.config.get("jsonSocket", "protocol"))
				logging.debug("cannot initialize %s-socket", globals.config.get("jsonSocket", "protocol"), exc_info=True)
				# Without connection, plugin couldn't work
				return

			else:
				# toDo is equals for all types, so only check if typ is supported
				supportedTypes = ["FMS", "ZVEI", "POC"]
				if typ in supportedTypes:
					logging.debug("Start %s to %s", typ, globals.config.get("jsonSocket", "protocol"))
					try:
						# dump data to json-string
						sendData = json.dumps(data)
						# send data
						sock.sendto(sendData, (globals.config.get("jsonSocket", "server"), globals.config.getint("jsonSocket", "port")))
					except:
						logging.error("%s to %s failed", typ, globals.config.get("jsonSocket", "protocol"))
						logging.debug("%s to %s failed", typ, globals.config.get("jsonSocket", "protocol"), exc_info=True)
						return

				else:
					logging.warning("Invalid Typ: %s", typ)	

			finally:
				logging.debug("close %s-Connection", globals.config.get("jsonSocket", "protocol"))
				try: 
					sock.close()
				except:
					pass
			
	except:
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)