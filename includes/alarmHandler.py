#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals  # Global variables

def processAlarm(typ,freq,data):
	logging.debug("[  ALARM  ]")
	for pluginName, plugin in globals.pluginList.items():
		from includes import filter
		if filter.checkFilters(data,typ,pluginName):	
			logging.debug("call Plugin: %s", pluginName)
			plugin.run(typ,freq,data)
			logging.debug("return from: %s", pluginName)
	logging.debug("[END ALARM]")