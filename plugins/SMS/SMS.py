#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
This plugin enables the function of sendig SMS to
a given number defined in config.ini
It is sensitive to ric and subric, also defined in
config.ini

@author: Jens Herrmann
@author: Bastian Schroll
@author: Florian Thillmann

@requires: Installed and configured gammu, SMS-gateway (such as UMTS-stick) working as non-root
"""

#
# Imports
#
import logging # Global logger
from includes import globalVars  # Global variables

# Helper function, uncomment to use
#from includes.helper import timeHandler
#from includes.helper import wildcardHandler
from includes.helper import configHandler

# import for gammu
import gammu

def find(l, elem):
    for row, i in enumerate(l):
        try:
            column = i.index(elem)
        except ValueError:
            continue
        return row, column
    return -1

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
		pass
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
	"""
	This function is the implementation of the Plugin.

	If necessary the configuration hast to be set in the config.ini.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  If necessary the configuration hast to be set in the config.ini.

	@return:    nothing
	@exception: nothing, make sure this function will never thrown an exception
	"""
	try:
		if configHandler.checkConfig("SMS"): #read and debug the config (let empty if no config used)
			if typ == "POC": # only available for POC!
				logging.debug("Plugin SMS enabled")

				# get number of cases and build a RIC-Array
				i = globalVars.config.get("SMS","quantity")
				aRic = []

				# build the array
				for x in range (1, int(i) + 1):
					# check the number of subrics
					subric = globalVars.config.get("SMS","subric" + str(x))
					if len(subric) > 1: # we have more than one subric
						subric_list = subric.split(",")
						for y in range (0, len(subric_list)):
							sric = subric_list[y].replace(' ','')
							full_ric = globalVars.config.get("SMS","ric" + str(x)) + sric
							case = x
							tmp = []
							tmp.append(full_ric)
							tmp.append(case)
							aRic.append(tmp)
					else:
						#get ric AND subric at once with ONE subric
						tmp = []
						tmp.append(globalVars.config.get("SMS","ric" + str(x)) + subric)
						tmp.append(x)
						aRic.append(tmp) # 2D-Array...

				# Debug: Display the multidimensional array aRic
				#logging.debug("aRic: %s", aRic)

				target = data["ric"] + data["functionChar"]

				#logging.debug("Searching for any occurences of %s", target)
				#if target in aRic:
				try:
					index = find(aRic, target)
				except:
					logging.error("RIC not found")

				logging.debug("Return from find: %s", index)
				if index != -1:
					case = aRic[index[0]][1]
					logging.debug("Enabling case %s", case)

					text = globalVars.config.get("SMS","text" + str(case))
					number = globalVars.config.get("SMS","phonenumber" + str(case))

					#just for debug
					logging.debug("Aktivierter Text: %s", text)
					logging.debug("Aktivierte Nummer: %s", number)

					# send sms
					try:
						sm = gammu.StateMachine()
						sm.ReadConfig()
						sm.Init()

						message = {
							'Text': text,
							'SMSC': {'Location': 1},
							'Number': number,
						}
						sm.SendSMS(message)
					except:
						logging.error("Failed to send SMS")
					else:
						logging.debug("Falsche SUB-RIC entdeckt - weiter gehts!")

			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
