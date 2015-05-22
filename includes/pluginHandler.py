#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals  # Global variables
from includes import pluginloader

def throwAlarm(typ,freq,data):
	logging.debug("[  ALARM  ]")
	for name, plugin in globals.pluginList.items():
		logging.debug("call Plugin: %s", name)
		plugin.run(typ,freq,data)
	logging.debug("[END ALARM]")

	
def loadPlugins():
	try:
		#load plugins
		logging.debug("loading plugins")
		for i in pluginloader.getPlugins():
			plugin = pluginloader.loadPlugin(i)
			globals.pluginList[i["name"]] = plugin
			
	except:
		logging.exception("cannot load Plugins")