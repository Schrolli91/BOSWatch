#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

def run(typ,freq,data):
	try:
		if typ == "ZVEI":
			logging.info("ZVEI: %s wurde auf %s empfangen!", data["zvei"],freq)
	except:
		logging.exception("Error in Template Plugin")