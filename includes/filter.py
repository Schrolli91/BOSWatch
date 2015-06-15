#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Functions for the RegEX filter

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger

import re #Regex for Filter Check

from includes import globals  # Global variables


def loadFilters():
	"""
	load all filters from the config.ini into globals.filterList

	@requires:  Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if filter loading failed
	"""
	try:
		logging.debug("loading filters")
		# For each entry in config.ini [Filters] section
		for key,val in globals.config.items("Filters"):
			logging.debug(" - %s = %s", key, val)
			filter = val.split(";")
			# insert splitet data into globals.filterList
			globals.filterList.append({"name": key, "typ": filter[0], "dataField": filter[1], "plugin": filter[2], "freq": freqToHz(filter[3]), "regex": filter[4]})
	except:
		logging.exception("cannot read config file")
	
	
def checkFilters(typ,data,plugin,freq):
	"""
	Check the Typ/Plugin combination with the RegEX filter
	If no filter for the combination is found, function returns True.
	
	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter
	@type    plugin: string
	@param   plugin: Name of the plugin to checked
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	
	@requires:  all filters in the filterList
	
	@return:    nothing
	@exception: Exception if filter check failed
	"""
	try:
		logging.debug("search Filter for %s to %s at %s Hz", typ, plugin, freq)
		
		foundFilter = False
		# go to all filter in globals.filterList
		for i in globals.filterList:
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
			return True
			
	except:
		logging.exception("Error in Filter checking")