#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import re
import datetime
import os

from includes import globals  # Global variables
from includes.helper import configHandler

##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	return


##
#
# Main function
# will be called by the alarmHandler
#
def run(typ,freq,data):
	try:
		if configHandler.checkConfig("Timecheck"): #read and debug the config
			if globals.config.get("Timecheck", "regex"):
				if typ == "POC":
					logging.debug("Timecheck via POC")
					now = datetime.datetime.now()
					p = re.compile(globals.config.get("Timecheck", "regex"))
					foundtime = p.match(data["msg"])
					#foundtime = re.match(r+configHandler.checkConfig("Timecheck","regex"), data["msg"])
					if foundtime:
						logging.debug("Found Time %s",foundtime.group(2))
						newtime = '%s-%s-%s %s:%s:00.000' % (now.year,now.month,now.day,foundtime.group(3),foundtime.group(4))
						logging.debug("Set Time to %s",newtime)
						os.system('sudo date --set="%s"' % newtime)
					else:
						logging.debug("No Time found")
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
