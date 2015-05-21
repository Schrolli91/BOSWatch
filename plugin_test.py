#!/usr/bin/python
# -*- coding: cp1252 -*-

import time
import pluginloader

import os #for absolute path: os.path.dirname(os.path.abspath(__file__))

import logging
import globals

import ConfigParser #for parse the config file

#create new logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#set log string format
formatter = logging.Formatter('%(asctime)s - %(module)-12s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')

#create a display loger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG) #log level >= info
ch.setFormatter(formatter)
logger.addHandler(ch)

#https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
#log levels
#----------
#debug - debug messages only for log
#info - information for normal display
#warning
#error - normal error - program goes further
#exception - error with exception message in log
#critical - critical error, program exit


#ConfigParser
logging.debug("reading config file")
try:
	globals.config = ConfigParser.ConfigParser()
	globals.config.read(globals.script_path+"./config/config.ini")
except:
	logging.exception("cannot read config file")


data = {"zvei":"12345"}
#data = {"ric":"1234567", "function":"1", "msg":"Hello World!"}


logging.debug("Load Plugins...")

pluginList = {}
for i in pluginloader.getPlugins():
			plugin = pluginloader.loadPlugin(i)
			pluginList[i["name"]] = plugin
	
logging.debug("All loaded...")	
	
while True:
	try:
		time.sleep(1)
		logging.info(" = = = = = = = = = ")
		logging.info("Alarm!")
		for name, plugin in pluginList.items():
			logging.debug("call Plugin: %s", name)
			plugin.run("ZVEI","0",data)
	except:
		logging.exception("Cannot Throw Modules")
		exit()