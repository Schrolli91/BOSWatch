#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals  # Global variables

def processAlarm(typ,freq,data):
	try:
		logging.debug("[  ALARM  ]")
		for pluginName, plugin in globals.pluginList.items():
		
			#if enabled use RegEx-Filter
			if globals.config.getint("BOSWatch","useRegExFilter"):
				from includes import filter
				if filter.checkFilters(data,typ,pluginName):	
					logging.debug("call Plugin: %s", pluginName)
					plugin.run(typ,freq,data)
					logging.debug("return from: %s", pluginName)
					
			else:
				logging.debug("call Plugin: %s", pluginName)
				plugin.run(typ,freq,data)
				logging.debug("return from: %s", pluginName)
				
		logging.debug("[END ALARM]")
	except:
		logging.exception("Error in Alarm processing")