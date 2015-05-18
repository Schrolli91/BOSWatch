#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables
import imp
import os

PluginFolder = "./plugins"
MainModule = "__init__"

def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        # plugins have to be a subdir with MainModule, if not skip
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        logging.debug("found plugin: "+i)

        # is the plugin enabled in the config-file?
        try: 
            usePlugin = int(globals.config.get("Module", i))
        except: #no entry for plugin found in config-file, skip
            continue
        logging.debug("use Plugin: "+str(usePlugin))
        if usePlugin:
            info = imp.find_module(MainModule, [location])
            plugins.append({"name": i, "info": info})
            logging.debug("append Plugin: "+i)
    return plugins

def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])