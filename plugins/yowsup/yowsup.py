#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Yowsup-Plugin to dispatch POCSAG - messages to WhatsApp Numbers or Chats

@author: fwmarcel

@requires: 	yowsup2 has to be installed
			whatsapp number and password
			yowsup-Configuration has to be set in the config.ini
"""

#
# Imports
#
import logging # Global logger
import sys, subprocess
import shlex

from includes import globals  # Global variables

# Helper function, uncomment to use
#from includes.helper import timeHandler
#from includes.helper import wildcardHandler
from includes.helper import configHandler

##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine is called one time for initialize the plugin

	@requires:  nothing

	@return:    nothing
	@exception: Exception if init has an fatal error so that the plugin couldn't work

	"""
	try:
		########## User onLoad CODE ##########
		pass
		########## User onLoad CODE ##########
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
		raise

##
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	try:
		if configHandler.checkConfig("yowsup"): #read and debug the config (let empty if no config used)

			########## User Plugin CODE ##########
			if typ == "FMS":
				logging.warning("%s not supported", typ)
			elif typ == "ZVEI":
				logging.warning("%s not supported", typ)
			elif typ == "POC":
				try:
					logging.debug("Try to send message")
					devnull = open('/dev/null', 'w')
					yowsup = subprocess.Popen(shlex.split('yowsup-cli demos -l' +globals.config.get("yowsup","sender")+ ':' + globals.config.get("yowsup","password") + ' --send ' +globals.config.get("yowsup","empfaenger") +' "' + data["msg"] +'"'), stdout=devnull)
					logging.debug("Message has been sent")
				except:
					logging.error("Message not send")
					logging.debug("Message not send")
					return
			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
