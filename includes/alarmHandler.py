#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Handler for the filter and plugins at an alarm

@author: Bastian Schroll
@author: Jens Herrmann

@requires: none
"""

import logging # Global logger
import time    # timestamp

from includes import globalVars  # Global variables
from copy import deepcopy

##
#
# decide to run AlarmHandler sync or async
#
def processAlarmHandler(typ, freq, data):
	"""
	Function to decide if the alarm process will call sync

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter

	@requires:  active plugins in pluginList
	@requires:  Configuration has to be set in the config.ini

	@return:    nothing
	@exception: Exception if starting a Thread failed
	"""
	if globalVars.config.getboolean("BOSWatch","processAlarmAsync") == True:
		logging.debug("starting processAlarm async")
		try:
			from threading import Thread
			Thread(target=processAlarm, args=(typ, freq, data)).start()
		except:
			logging.error("Error in starting alarm processing async")
			logging.debug("Error in starting alarm processing async", exc_info=True)
	else:
		processAlarm(typ, freq, data)


##
#
# main function for central filtering and calling the plugins
#
def processAlarm(typ, freq, data):
	"""
	Function to process filters and plugins at Alarm

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter

	@requires:  active plugins in pluginList

	@return:    nothing
	@exception: Exception if Alarm processing itself failed
	"""
	try:
		logging.debug("[  ALARM  ]")
		# timestamp, to make sure, that all plugins use the same time
		data['timestamp'] = int(time.time())
		#copy objects to avoid issues if the objects will be changed by the plugin's during runtime or during asynch/threaded processing 
		dctyp = deepcopy(typ)
		dcfreq = deepcopy(freq)
		dcdata = deepcopy(data)
		# Go to all plugins in pluginList
		for pluginName, plugin in globalVars.pluginList.items():
			# if enabled use RegEx-filter
			if globalVars.config.getint("BOSWatch","useRegExFilter"):
				from includes import regexFilter
				if regexFilter.checkFilters(dctyp, dcdata, pluginName, dcfreq):
					logging.debug("call Plugin: %s", pluginName)
					try:
						plugin.run(dctyp, dcfreq, dcdata)
						logging.debug("return from: %s", pluginName)
					except:
						# call next plugin, if one has thrown an exception
						pass
			else: # RegEX filter off - call plugin directly
				logging.debug("call Plugin: %s", pluginName)
				try:
					plugin.run(dctyp, dcfreq, dcdata)
					logging.debug("return from: %s", pluginName)
				except:
					# call next plugin, if one has thrown an exception
					pass
		logging.debug("[END ALARM]")
	except:
		logging.error("Error in alarm processing")
		logging.debug("Error in alarm processing", exc_info=True)
