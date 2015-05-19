#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables
import imp
import os

PluginFolder = "./plugins"

def getPlugins():
	plugins = []
	possibleplugins = os.listdir(PluginFolder)
	for i in possibleplugins:
		location = os.path.join(PluginFolder, i)
		# plugins have to be a subdir with MainModule, if not skip
		if not os.path.isdir(location) or not i + ".py" in os.listdir(location):
			continue
		logging.debug("found Plugin: %s", i)

		# is the plugin enabled in the config-file?
		try: 
			usePlugin = int(globals.config.get("Plugins", i))
		except: #no entry for plugin found in config-file, skip
			logging.warning("Plugin not in config: %s", i)
			

		if usePlugin:
			info = imp.find_module(i, [location])
			plugins.append({"name": i, "info": info})
			logging.debug("use Plugin: %s", i)
	return plugins

def loadPlugin(plugin):
	logging.debug("load Plugin: %s", plugin["name"])
	return imp.load_module(plugin["name"], *plugin["info"])