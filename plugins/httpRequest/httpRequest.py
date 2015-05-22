#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

#########
# USAGE
#
#	Config
# ======
# to read a option from config File
# VALUE = globals.config.get("SECTION", "OPTION")
#
# Data from boswatch.py
# =====================
# use data["KEY"] for Alarm Data from boswatch.py
# for usable KEYs in different Functions (FMS|ZVEI|POC) see interface.txt
#
# LOG Messages
# ============
# send Log Messages with logging.LOGLEVEL("MESSAGE")
# usable Loglevels debug|info|warning|error|exception|critical
# if you use .exception in Try:Exception: Construct, it logs the Python EX.message too

def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("httpRequest"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
	
########## User Plugin CODE ##########		
		if typ == "FMS":
			logging.warning("%s not supported", typ)
		elif typ == "ZVEI":
			logging.warning("%s not supported", typ)
		elif typ == "POC":
			logging.warning("%s not supported", typ)
		else:
			logging.warning("Invalid Typ: %s", typ)	
########## User Plugin CODE ##########
			
	except:
		logging.exception("unknown error")
