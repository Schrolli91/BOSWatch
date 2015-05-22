#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import imp
import os

from includes import globals  # Global variables


def getPlugins():
	try:
		logging.debug("Search in Plugin Folder")
		PluginFolder = globals.script_path+"/plugins"
		plugins = []
		for i in os.listdir(PluginFolder):
			location = os.path.join(PluginFolder, i)
			# plugins have to be a subdir with MainModule, if not skip
			if not os.path.isdir(location) or not i + ".py" in os.listdir(location):
				continue

			# is the plugin enabled in the config-file?
			try: 
				if globals.config.getint("Plugins", i):
					info = imp.find_module(i, [location])
					plugins.append({"name": i, "info": info})
					logging.debug("Plugin [ENABLED ] %s", i)
				else:
					logging.debug("Plugin [DISABLED] %s ", i)
			except: #no entry for plugin found in config-file, skip
				logging.warning("Plugin [NO CONF ] %s", i)				
	except:
		logging.exception("Error during Plugin search")

	return plugins

def loadPlugin(plugin):
	try:
		logging.debug("load Plugin: %s", plugin["name"])
		return imp.load_module(plugin["name"], *plugin["info"])
	except:
		logging.exception("cannot load Plugin: %s", plugin["name"])