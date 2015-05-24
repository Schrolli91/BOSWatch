#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger

import re #Regex for Filter Check

from includes import globals  # Global variables


def getFilters():
	logging.debug("reading config file")
	try:
		for key,val in globals.config.items("Filters"):
			logging.debug(" - %s = %s", key, val)
			filter = val.split(";")
			globals.filterList.append({"name": key, "typ": filter[0], "plugin": filter[1], "regex": filter[2]})
	except:
		logging.exception("cannot read config file")
	
	
def checkFilters(data,typ,plugin):
	try:
		logging.debug("search Filter for %s to %s", typ, plugin)
		
		#extract the correct data for filtering
		#if typ == "FMS": data = data["fms"]
		#if typ == "ZVEI": data = data["zvei"]
		#if typ == "POC": data = data["poc"]
		
		foundFilter = False
		for i in globals.filterList:
			if i["typ"] == typ and i["plugin"] == plugin:
				foundFilter = True
				logging.debug("found Filter: %s = %s", i["name"], i["regex"])
				if re.search(i["regex"], data[typ.lower()]):
					logging.debug("Filter passed: %s", i["name"])
					return True
				else:
					logging.debug("Filter not passed: %s", i["name"])
			
		if foundFilter:
			logging.debug("no Filter passed")
			return False
		else:
			logging.debug("no Filter found")
			return True
			
	except:
		logging.exception("Error in Filter checking")