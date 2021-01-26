#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Functions for the location RegEX

@author: Marco Schotthöfer

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import re #Regex for Filter Check

from includes import globalVars  # Global variables

# local variables
filterList = []


def loadFilters():
	try:
		logging.debug("Loading location coordinates")
		
		for key,val in globalVars.config.items("LocationCoordinates"):
			logging.debug(" - %s = %s", key, val)
			filterData = val.split(";")

			# at least 3 items needed (field1;pattern1;lat,lon), and in any case an uneven count of items
			if len(filterData) < 3 and len(filterData) % 2 == 0:
				logging.debug("Invalid argument count; skipping")
			else:
				# first store all regular expressions in list
				filterItem = []
				i = 0
				
				while i < len(filterData) - 2:
					filterItem.append({"field": filterData[i], "pattern": filterData[i+1]})
					
					# step to next field
					i += 2
			# then transfer to filterList; include coordinates
			filterList.append({"name": key, "filterItem": filterItem, "coordinates": filterData[len(filterData) - 1]})
	except:
		logging.error("cannot read config file")
		logging.debug("cannot read config file", exc_info=True)
		return

def findCoordinates(data):
	try:
		logging.debug("Find coordinates")
		for i in filterList:
			logging.debug("Filter: " + str(i))
			regexMatch = True
			for k in i["filterItem"]:
				logging.debug("Pattern : " + str(k))
				if k["field"] not in data.keys():
					logging.debug("Field " + k["field"] + " not in data structure, hence no match")
					regexMatch = False
					break
				else:
					if not re.search(k["pattern"], data.get(k["field"])):
						logging.debug("No match")
						regexMatch = False
						break
			if regexMatch:
				coordinatesString = i["coordinates"]
				logging.debug("Coordinates string: " + coordinatesString)
				coordinatesList = coordinatesString.replace(" ", "").split(",")
				if len(coordinatesList) == 2:
					data["lat"] = coordinatesList[0]
					data["lon"] = coordinatesList[1]
					data["has_geo"] = True
					logging.info("Coordinates found!")
					break
	except:
		logging.error("cannot read config file")
		logging.debug("cannot read config file", exc_info=True)
