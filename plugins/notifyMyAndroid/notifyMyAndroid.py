#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
notifyMyAndroid-Plugin to dispatch FMS-, ZVEI- and POCSAG-messages via UDP/TCP

@author: Jens Herrmann

@requires: notifyMyAndroid-Configuration has to be set in the config.ini
"""

import logging # Global logger
import csv     # for loading the APIKeys


from includes import globalVars  # Global variables

from includes.helper import configHandler
from includes.helper import timeHandler
from includes.helper import stringConverter
from includes.pynma import pynma


# local variables
application = "BOSWatch"
APIKey = None
remainingMsgs = None
usecsv = False
# data structures: xAPIKeyList[id][i] = (APIKey, priority, eventPrefix)
fmsAPIKeyList = {}
zveiAPIKeyList = {}
pocAPIKeyList = {}


def checkResponse(response, APIKey):
	"""
	Helper function to check the response of NMA

	@type    response: dict
	@param   response: Response of the pyNMA.push() method
	@type    data: string / array
	@param   data: a string containing 1 key or an array of keys

	@return:    nothing
	"""
	# local variables
	global remainingMsgs
	try:
		#
		# check HTTP-Response
		#
		if str(response[APIKey]['code']) == "200": #Check HTTP Response an print a Log or Error
			logging.debug("NMA response: %s" , str(response[APIKey]['code']))
			remainingMsgs = response[APIKey]['remaining']
			if int(remainingMsgs) == 0:
				logging.error("NMA remaining msgs: %s" , str(remainingMsgs))
			if int(response[APIKey]['remaining']) < 20:
				logging.warning("NMA remaining msgs: %s" , str(remainingMsgs))
			else:
				logging.debug("NMA remaining msgs: %s" , str(remainingMsgs))
		else:
			logging.warning("NMA response: %s - %s" , str(response[APIKey]['code']), str(response[APIKey]['message']))
	except:
		logging.error("cannot read pynma response")
		logging.debug("cannot read pynma response", exc_info=True)
		return


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
	"""
	# local variables
	global application
	global APIKey
	global usecsv

	# load config:
	configHandler.checkConfig("notifyMyAndroid")
	application = stringConverter.convertToUnicode(globalVars.config.get("notifyMyAndroid","appName"))
	usecsv = globalVars.config.getboolean("notifyMyAndroid","usecsv")

	# if no csv should use, we take the APIKey directly
	if usecsv == False:
		APIKey = globalVars.config.get("notifyMyAndroid","APIKey")
	else:
		# import the csv-file
		try:
			logging.debug("-- loading nma.csv")
			with open(globalVars.script_path+'/csv/nma.csv') as csvfile:
				# DictReader expected structure described in first line of csv-file
				reader = csv.DictReader(csvfile)
				for row in reader:
					logging.debug(row)
					# only import rows with an supported types
					supportedTypes = ["FMS", "ZVEI", "POC"]
					if row['typ'] in supportedTypes:
						try:
							if "FMS" in row['typ']:
								# if len for id in mainList raise an KeyErrorException, we have to init it...
								try:
									if len(fmsAPIKeyList[row['id']]) > 0:
										pass
								except KeyError:
									fmsAPIKeyList[row['id']] = []
								# data structure: fmsAPIKeyList[fms][i] = (APIKey, priority)
								fmsAPIKeyList[row['id']].append((row['APIKey'], row['priority'], row['eventPrefix']))

							elif "ZVEI" in row['typ']:
								# if len for id in mainList raise an KeyErrorException, we have to init it...
								try:
									if len(zveiAPIKeyList[row['id']]) > 0:
										pass
								except KeyError:
									zveiAPIKeyList[row['id']] = []
								# data structure: zveiAPIKeyList[zvei][i] = (APIKey, priority)
								zveiAPIKeyList[row['id']].append((row['APIKey'], row['priority'], row['eventPrefix']))

							elif "POC" in row['typ']:
								# if len for id in mainList raise an KeyErrorException, we have to init it...
								try:
									if len(pocAPIKeyList[row['id']]) > 0:
										pass
								except KeyError:
									pocAPIKeyList[row['id']] = []
								# data structure: zveiAPIKeyList[ric][i] = (APIKey, priority)
								pocAPIKeyList[row['id']].append((row['APIKey'], row['priority'], row['eventPrefix']))

						except:
							# skip entry in case of an exception
							logging.debug("error in shifting...", exc_info=True)
					# if row['typ'] in supportedTypes
				# for row in reader:
			logging.debug("-- loading csv finished")
		except:
			logging.error("loading csvList for nma failed")
			logging.debug("loading csvList for nma failed", exc_info=True)
			raise
	# and if usecsv == True
	return


##
#
# Main function of jsonSocket-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the notifyMyAndroid-Plugin.

	The configuration is set in the config.ini.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending via UDP/TCP
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch to UDP.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  notifyMyAndroid-Configuration has to be set in the config.ini

	@return:    nothing
	"""
	# local variables

	try:
		try:
			#
			# initialize to pyNMA
			#
			nma = pynma.PyNMA()
		except:
			logging.error("cannot initialize pyNMA")
			logging.debug("cannot initialize pyNMA", exc_info=True)
			# Without class, plugin couldn't work
			return

		else:
			# toDo is equals for all types, so only check if typ is supported
			supportedTypes = ["FMS", "ZVEI", "POC"]
			if typ in supportedTypes:
				logging.debug("Start %s to NMA", typ)
				try:
					# build event and msg
					# pyNMA expect strings are not in UTF-8
					event = stringConverter.convertToUnicode(data['description'])
					msg   = timeHandler.getDateTime(data['timestamp'])
					if ("POC" in typ) and (len(data['msg']) > 0):
						msg += "\n" + data['msg']
					msg = stringConverter.convertToUnicode(msg)

					# if not using csv-import, all is simple...
					if usecsv == False:
						response = nma.pushWithAPIKey(APIKey, application, event, msg, priority=globalVars.config.getint("notifyMyAndroid","priority"))
						checkResponse(response, APIKey)
					else:
						if "FMS" in typ:
							# lets look for fms in fmsAPIKeyList
							xID = data['fms']
							try:
								# data structure: fmsAPIKeyList[xID][i] = (xAPIKey, xPriority, xEventPrefix)
								for i in range(len(fmsAPIKeyList[xID])):
									xEvent = event
									(xAPIKey, xPriority, xEventPrefix) = fmsAPIKeyList[xID][i]
									if len(xEventPrefix) > 0:
										xEvent = xEventPrefix + ": " + xEvent
									response = nma.pushWithAPIKey(xAPIKey, application, xEvent, msg, priority=xPriority)
									checkResponse(response, xAPIKey)
							except KeyError:
								# nothing found
								pass

						elif "ZVEI" in typ:
							# lets look for zvei in zveiAPIKeyList
							xID = data['zvei']
							try:
								# data structure: zveiAPIKeyList[xID][i] = (xAPIKey, xPriority, xEventPrefix)
								for i in range(len(zveiAPIKeyList[xID])):
									xEvent = event
									(xAPIKey, xPriority, xEventPrefix) = zveiAPIKeyList[xID][i]
									if len(xEventPrefix) > 0:
										xEvent = xEventPrefix + ": " + xEvent
									response = nma.pushWithAPIKey(xAPIKey, application, xEvent, msg, priority=xPriority)
									checkResponse(response, xAPIKey)
							except KeyError:
								# nothing found
								pass

						elif "POC" in typ:
							xID = ""
							# 1. lets look for ric+functionChar in pocAPIKeyList
							try:
								xID = data['ric'] + data['functionChar']
								# data structure: pocAPIKeyList[xID][i] = (xAPIKey, xPriority, xEventPrefix)
								for i in range(len(pocAPIKeyList[xID])):
									xEvent = event
									(xAPIKey, xPriority, xEventPrefix) = pocAPIKeyList[xID][i]
									if len(xEventPrefix) > 0:
										xEvent = xEventPrefix + ": " + xEvent
									response = nma.pushWithAPIKey(xAPIKey, application, xEvent, msg, priority=xPriority)
									checkResponse(response, xAPIKey)
							except KeyError:
								# nothing found
								pass
							# 2. lets look for ric* in pocAPIKeyList
							try:
								xID = data['ric'] + "*"
								# data structure: pocAPIKeyList[xID][i] = (xAPIKey, xPriority, xEventPrefix)
								for i in range(len(pocAPIKeyList[xID])):
									xEvent = event
									(xAPIKey, xPriority, xEventPrefix) = pocAPIKeyList[xID][i]
									if len(xEventPrefix) > 0:
										xEvent = xEventPrefix + ": " + xEvent
									response = nma.pushWithAPIKey(xAPIKey, application, xEvent, msg, priority=xPriority)
									checkResponse(response, xAPIKey)
							except KeyError:
								# nothing found
								pass
							# 3. lets look for ric prefixes in pocAPIKeyList
                                                        for prefixLength in reversed(range(6)):
                                                                ricPrefix = data['ric'][:prefixLength]
                                                                #fill the ric with stars
                                                                ricPrefix = ricPrefix.ljust(8,'*')
                                                                try:
                                                                        xID = ricPrefix
                                                                        # data structure: pocAPIKeyList[xID][i] = (xAPIKey, xPriority, xEventPrefix)
                                                                        for i in range(len(pocAPIKeyList[xID])):
                                                                                xEvent = event
                                                                                (xAPIKey, xPriority, xEventPrefix) = pocAPIKeyList[xID][i]
                                                                                if len(xEventPrefix) > 0:
                                                                                        xEvent = xEventPrefix + ": " + xEvent
                                                                                response = nma.pushWithAPIKey(xAPIKey, application, xEvent, msg, priority=xPriority)
                                                                                checkResponse(response, xAPIKey)
                                                                except KeyError:
                                                                        # nothing found
                                                                        pass

						# end if "POC" in typ
					# end if usecsv == True
				except:
					logging.error("%s to NMA failed", typ)
					logging.debug("%s to NMA failed", typ, exc_info=True)
					return
			else:
				logging.warning("Invalid Typ: %s", typ)

	except:
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
