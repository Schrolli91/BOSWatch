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
	@exception: Exception if ConfigParser failed
	@exception: Exception if connect to socket-Server failed
	@exception: Exception if sending the socket-message failed
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
			logging.exception("cannot read config file")

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
			logging.exception("cannot initialize %s-socket", globals.config.get("jsonSocket", "protocol"))

		else:

			supportedTypes = ["FMS", "ZVEI", "POC"]
			if typ in supportedTypes:
				logging.debug("Start %s to %s", typ, globals.config.get("jsonSocket", "protocol"))
				try:
					# convert data to json
					sendData = json.dumps(data)
					# send data
					sock.sendto(sendData, (globals.config.get("jsonSocket", "server"), globals.config.getint("jsonSocket", "port")))
				except:
					logging.exception("%s to %s failed", typ, globals.config.get("jsonSocket", "protocol"))

			else:
				logging.warning("Invalid Typ: %s", typ)	

		finally:
			logging.debug("close %s-Connection", globals.config.get("jsonSocket", "protocol"))
			sock.close()
			
	except:
		logging.exception("")