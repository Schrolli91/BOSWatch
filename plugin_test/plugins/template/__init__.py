#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

def run(typ,freq,data):
	try:
		logging.debug("read config file")
		data1 = globals.config.get("template", "data1")
		data2 = globals.config.get("template", "data2")
		data3 = globals.config.get("template", "data3")
		data4 = globals.config.get("template", "data4")
		logging.debug(" - Data1: %s", data1)
		logging.debug(" - Data2: %s", data2)
		logging.debug(" - Data3: %s", data3)
		logging.debug(" - Data4: %s", data4)
	
		if typ == "FMS":
			logging.debug("FMS: %s Status: %s Dir: %s", data["fms"], data["status"], data["direction"])
		elif typ == "ZVEI":
			logging.debug("ZVEI: %s", data["zvei"])
		elif typ == "POC":
			logging.debug("POC: %s/%s - %s", data["ric"], data["function"], data["msg"])
		else:
			logging.warning(typ + " not supportet")
			
	except:
		logging.exception("unknown error")