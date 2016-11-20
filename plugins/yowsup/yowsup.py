#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Yowsup-Plugin to dispatch POCSAG - messages to WhatsApp Numbers or Chats

@author: fwmarcel

@requires: 	yowsup2 has to be installed
			whatsapp number and password
			yowsup-Configuration has to be set in the config.ini
"""

import logging
import subprocess
import shlex
import os

from includes import globalVars

#from includes.helper import timeHandler
from includes.helper import wildcardHandler
from includes.helper import configHandler


def onLoad():
	return

def run(typ,freq,data):
	try:
		if configHandler.checkConfig("yowsup"):

			empfaenger = globalVars.config.get("yowsup", "empfaenger")
			sender = globalVars.config.get("yowsup", "sender")
			password = globalVars.config.get("yowsup", "password")
			devnull = open(os.devnull, "wb")

			if typ == "FMS":
					text = globalVars.config.get("yowsup","fms_message")
					text = wildcardHandler.replaceWildcards(text, data)
					cmd = 'yowsup-cli demos -l ' + sender + ':' + password + ' -s ' + empfaenger + ' "' + text + '" -M'
					subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
					logging.debug("Message has been sent")
			elif typ == "ZVEI":
					text = globalVars.config.get("yowsup","zvei_message")
					text = wildcardHandler.replaceWildcards(text, data)
					cmd = 'yowsup-cli demos -l ' + sender + ':' + password + ' -s ' + empfaenger + ' "' + text + '" -M'
					subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
					logging.debug("Message has been sent")
			elif typ == "POC":
				try:
					text = globalVars.config.get("yowsup","poc_message")
					text = wildcardHandler.replaceWildcards(text, data)
					cmd = 'yowsup-cli demos -l ' + sender + ':' + password + ' -s ' + empfaenger + ' "' + text + '" -M'
					subprocess.call(shlex.split(cmd), stdout=devnull, stderr=devnull)
					logging.debug("Message has been sent")
				except:
					logging.error("Message not send")
					logging.debug("Message not send")
					return
			else:
				logging.warning("Invalid Typ: %s", typ)

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
