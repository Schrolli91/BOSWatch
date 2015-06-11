#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
firEmergency-Plugin to dispatch ZVEI- and POCSAG - messages to firEmergency

@autor: Smith-fms

@requires: firEmergency-Configuration has to be set in the config.ini
"""

import logging # Global logger
import socket

from includes import globals  # Global variables

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
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to firEmergency.
	@type    freq: string
	@keyword freq: frequency is not used in this plugin

	@requires:  firEmergency-Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if ConfigParser failed
	@exception: Exception ifconnect to firEmergency failed
	@exception: Exception if sending the data failed
	"""
	try:
		#
		#ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("firEmergency"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")

		try:
			#
			# connect to firEmergency
			#
			firSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			firSocket.connect((globals.config.get("firEmergency", "firserver"), globals.config.getint("firEmergency", "firport")))
		except:
			logging.exception("cannot connect to firEmergency")
		else:	
			#
			# Format given data-structure to xml-string for firEmergency
			#
			if typ == "FMS":
				logging.debug("FMS not supported by firEmgency")
				
			elif typ == "ZVEI":
				logging.debug("ZVEI to firEmergency")
				try:
						firXML = "<event>\n<address>"+data["zvei"]+"</address>\n<message>"+data["zvei"]+" alarmiert.</message>\n</event>\n"
						firSocket.send(firXML)
				except:
						logging.exception("ZVEI to firEmergency failed")  

			elif typ == "POC":
				logging.debug("POC to firEmergency")
				try:
						firXML = "<event>\n<address>"+data["ric"]+"</address>\n<message>"+data["msg"]+"</message>\n</event>\n"
						firSocket.send(firXML)
				except:
						logging.exception("POC to firEmergency failed")  

			else:
				logging.warning("Invalid Typ: %s", typ)	

		finally:
			logging.debug("close firEmergency-Connection")
			firSocket.close()

	except:
		logging.exception("unknown error")