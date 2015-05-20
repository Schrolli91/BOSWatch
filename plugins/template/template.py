#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("BOSWatch"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
	
		if typ == "FMS":
			logging.debug(typ + " not supported")
		elif typ == "ZVEI":
			logging.debug(typ + " not supported")
		elif typ == "POC":
			logging.debug(typ + " not supported")
		else:
			logging.warning(typ + " not supported")
			
	except:
		logging.exception("unknown error")