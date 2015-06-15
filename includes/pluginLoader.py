#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Functions to Load and import the Plugins

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import imp
import os

from ConfigParser import NoOptionError # we need this exception
from includes import globals  # Global variables

def loadPlugins():
	"""
	Load all Plugins into globals.pluginList

	@return:    nothing
	@exception: Exception if insert into globals.pluginList failed
	"""
	try:
		logging.debug("loading plugins")
		# go to all Plugins from getPlugins()
		for i in getPlugins():
			# call for each Plugin the loadPlugin() Methode
			plugin = loadPlugin(i)
			# Add it to globals.pluginList
			globals.pluginList[i["name"]] = plugin			
	except:
		logging.exception("cannot load Plugins")


def getPlugins():
	"""
	get a Python Dict of all activeated Plugins

	@return:    Plugins as Python Dict
	@exception: Exception if Plugin search failed
	"""
	try:
		logging.debug("Search in Plugin Folder")
		PluginFolder = globals.script_path+"/plugins"
		plugins = []
		# Go to all Folders in the Plugin-Dir
		for i in os.listdir(PluginFolder):
			location = os.path.join(PluginFolder, i)
				
			# Skip if Path.isdir() or no File DIR_NAME.py is found 
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
			# no entry for plugin found in config-file
			except NoOptionError: 
				logging.warning("Plugin [NO CONF ] %s", i)				
				pass
	except:
		logging.exception("Error during Plugin search")

	return plugins


def loadPlugin(plugin):
	"""
	Imports a single Plugin

	@type    plugin: Plugin Data
	@param   plugin: Contains the information to import a Plugin
	
	
	@return:    nothing
	@exception: Exception if Plugin import failed
	"""
	try:
		logging.debug("load Plugin: %s", plugin["name"])
		return imp.load_module(plugin["name"], *plugin["info"])
	except:
		logging.exception("cannot load Plugin: %s", plugin["name"])