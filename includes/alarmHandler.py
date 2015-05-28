#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Handler for the Filter and Plugins at an Alarm

@author: Bastian Schroll

@requires: none
"""

import logging # Global logger

from includes import globals  # Global variables


def processAlarm(typ,freq,data):
	"""
	Function to process Filters and Plugins at Alarm

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter

	@requires:  active Plugins in pluginList
	
	@return:    nothing
	@exception: Exception if Alarm processing failed
	"""
	try:
		logging.debug("[  ALARM  ]")
		#Go to all Plugins in pluginList
		for pluginName, plugin in globals.pluginList.items():
		
			#if enabled use RegEx-Filter
			if globals.config.getint("BOSWatch","useRegExFilter"):
				from includes import filter
				if filter.checkFilters(typ,data,pluginName,freq):	
					logging.debug("call Plugin: %s", pluginName)
					plugin.run(typ,freq,data)
					logging.debug("return from: %s", pluginName)
					
			else: #RegEX Filter off - Call Plugin direct
				logging.debug("call Plugin: %s", pluginName)
				plugin.run(typ,freq,data)
				logging.debug("return from: %s", pluginName)
				
		logging.debug("[END ALARM]")
	except:
		logging.exception("Error in Alarm processing")