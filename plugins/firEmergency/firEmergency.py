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
			logging.error("cannot read config file")
			logging.debug("cannot read config file", exc_info=True)
		else: # Without config, plugin couldn't work

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
							firXML = "<event>\n<address>"+data["zvei"]+"</address>\n<message>"+data["zvei"]+" alarmiert.</message>\n</event>\n"
							firSocket.send(firXML)
					except:
							logging.error("%s to firEmergency failed", typ)
							logging.debug("%s to firEmergency failed", typ, exc_info=True)
							# Without connection, plugin couldn't work
							return
							
				elif typ == "POC":
					logging.debug("POC to firEmergency")
					try:
							firXML = "<event>\n<address>"+data["ric"]+"</address>\n<message>"+data["msg"]+"</message>\n</event>\n"
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