#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Handler for the filter and plugins at an alarm

@author: Bastian Schroll
@author: Jens Herrmann

@requires: none
"""

import logging # Global logger

from includes import globals  # Global variables

##
#
# main function for central filtering and calling the plugins
#
def processAlarm(typ,freq,data):
	"""
	Function to process filters and plugins at Alarm

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter

	@requires:  active plugins in pluginList

	@return:    nothing
	@exception: Exception if Alarm processing itself failed
	"""
	try:
		logging.debug("[  ALARM  ]")
		# Go to all plugins in pluginList
		for pluginName, plugin in globals.pluginList.items():
			# if enabled use RegEx-filter
			if globals.config.getint("BOSWatch","useRegExFilter"):
				from includes import filter
				if filter.checkFilters(typ,data,pluginName,freq):
					logging.debug("call Plugin: %s", pluginName)
					try:
						plugin.run(typ,freq,data)
						logging.debug("return from: %s", pluginName)
					except:
						# call next plugin, if one has thrown an exception
						pass
			else: # RegEX filter off - call plugin directly
				logging.debug("call Plugin: %s", pluginName)
				try:
					plugin.run(typ,freq,data)
					logging.debug("return from: %s", pluginName)
				except:
					# call next plugin, if one has thrown an exception
					pass
		logging.debug("[END ALARM]")
	except:
		logging.exception("Error in alarm processing")
