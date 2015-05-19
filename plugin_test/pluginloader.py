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
		logging.debug("found plugin: "+i)

		# is the plugin enabled in the config-file?
		try: 
			usePlugin = int(globals.config.get("Module", i))
		except: #no entry for plugin found in config-file, skip
			logging.warning("Plugin not in config: "+i)
			
		logging.debug("use Plugin: "+str(usePlugin))
		if usePlugin:
			info = imp.find_module(i, [location])
			plugins.append({"name": i, "info": info})
			logging.debug("append Plugin: "+i)
	return plugins

def loadPlugin(plugin):
	return imp.load_module(plugin["name"], *plugin["info"])