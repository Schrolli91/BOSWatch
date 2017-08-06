#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Functions for the RegEX filter

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import re #Regex for Filter Check

from includes import globalVars  # Global variables
from includes.helper import freqConverter  # converter functions


# local variables
filterList = []


def loadFilters():
	"""
	load all filters from the config.ini into filterList

	@requires:  Configuration has to be set in the config.ini

	@return:    nothing
	"""
	try:
		logging.debug("loading filters")
		# For each entry in config.ini [Filters] section
		for key,val in globalVars.config.items("Filters"):
			logging.debug(" - %s = %s", key, val)
			filterData = val.split(";")

			# resolve the * for freqToHz()
			if not filterData[3] == "*":
				filterData[3] = freqConverter.freqToHz(filterData[3])

			# insert splitet data into filterList
			filterList.append({"name": key, "typ": filterData[0], "dataField": filterData[1], "plugin": filterData[2], "freq": filterData[3], "regex": filterData[4]})
	except:
		logging.error("cannot read config file")
		logging.debug("cannot read config file", exc_info=True)
		return


def checkFilters(typ, data, plugin, freq):
	"""
	Check the Typ/Plugin combination with the RegEX filter
	If no filter for the combination is found, function returns True.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter
	@type    plugin: string
	@param   plugin: Name of the plugin to checked
	@type    freq: string
	@param   freq: frequency of the SDR Stick

	@requires:  all filters in the filterList

	@return:    nothing
	"""
	global filterList
	try:
		logging.debug("search Filter for %s to %s at %s Hz", typ, plugin, freq)

		foundFilter = False
		# go to all filter in filterList
		for i in filterList:
			# if typ/plugin/freq combination is found
			if i["typ"] == typ and (i["plugin"] == plugin or i['plugin'] == "*") and (i["freq"] == freq or i['freq'] == "*"):
				foundFilter = True
				logging.debug("found Filter: %s = %s", i["name"], i["regex"])
				# Check the RegEX
				if re.search(i["regex"], data[i["dataField"]]):
					logging.debug("Filter passed: %s", i["name"])
					return True
				else:
					logging.debug("Filter not passed: %s", i["name"])

		if foundFilter:
			logging.debug("no Filter passed")
			return False
		else:
			logging.debug("no Filter found")
			return False

	except:
		logging.error("Error in filter checking")
		logging.debug("Error in filter checking", exc_info=True)
		# something goes wrong, data will path
		return True
