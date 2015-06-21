#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
json-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages via UDP

@author: Jens Herrmann

@requires: jsonUDP-Configuration has to be set in the config.ini
"""

import logging # Global logger

import socket # for udp-connection
import json # for data

from includes import globals  # Global variables

##
#
# Main function of jsonUDP-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the jsonUDP-Plugin.
	It will send the data via UDP
	
	The configuration for the UDP-Connection is set in the config.ini.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending via UDP
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to UDP.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  jsonUDP-Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if ConfigParser failed
	@exception: Exception if connect to UDP-Server failed
	@exception: Exception if sending the UDP-message failed
	"""
	try:
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("jsonUDP"):
				logging.debug(" - %s = %s", key, val)
				
		except:
			logging.exception("cannot read config file")

		try:
		    #
			# initialize to UDP-Server
			#
			# SOCK_DGRAM is the socket type to use for UDP sockets
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			
		except:
			logging.exception("cannot initialize UDP-socket")

		else:

			if typ == "FMS":
				logging.debug("Start FMS to UDP")
				try:
					# convert data to json
					sendData = json.dumps(data)
					# send UDP
					sock.sendto(sendData, (globals.config.get("jsonUDP", "server"), globals.config.getint("jsonUDP", "port")))
				except:
					logging.exception("FMS to UDP failed")

			elif typ == "ZVEI":
				logging.debug("Start ZVEI to UDP")
				try:
					# convert data to json
					sendData = json.dumps(data)
					# send UDP
					sock.sendto(sendData, (globals.config.get("jsonUDP", "server"), globals.config.getint("jsonUDP", "port")))
				except:
					logging.exception("ZVEI to UDP failed")

			elif typ == "POC":
				logging.debug("Start POC to UDP")
				try:
					# convert data to json
					sendData = json.dumps(data)
					# send UDP
					sock.sendto(sendData, (globals.config.get("jsonUDP", "server"), globals.config.getint("jsonUDP", "port")))
				except:
					logging.exception("POC to UDP failed")
			
			else:
				logging.warning("Invalid Typ: %s", typ)	

		finally:
			logging.debug("close UDP-Connection")
			sock.close()
			
	except:
		logging.exception("")