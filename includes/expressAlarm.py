#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
expressAlarm is the function to enable BOSwatch to deal with Swissfone Express-Alarm

@author: Fabian Kessler

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import time    # timestamp for expressAlarm

from includes import globalVars  # Global variables

expressList = []

def newEntryExpressList(eatyp, eapoc_id, eapoc_sub, eapoc_text):
	"""
	add entry to express alarm list and remove old entries

	@return:    nothing
	"""
	global expressList
	tmpexpressList = []
	timestamp = int(time.time())
	# Express-Alarm processing if enabled and delimiter RIC has been received
	if eapoc_id == globalVars.config.get("ExpressAlarm", "expressAlarm_delimiter_ric"):
		expressList = []
		logging.debug("Express-Alarm delimiter RIC received --> buffer cleared  %s  %s %s ", eapoc_id, eapoc_sub, eapoc_text)
	else:
		expressList.append([eatyp, eapoc_id, eapoc_sub, eapoc_text.strip(), timestamp])
		logging.debug("Added %s  %s %s to expressList", eapoc_id, eapoc_sub, eapoc_text)
		# check for old entries in expressList
		for i, exList in enumerate(expressList):
			# we have to remove entries older than timestamp - ignore time
			if int(exList[i][4]) > timestamp-globalVars.config.getint("ExpressAlarm", "expressAlarm_ignore_time"):
				tmpexpressList.append(exList[i])
	expressList = tmpexpressList


def expressAlarmExec(typ, freq, data):
	"""
	call alarmHandler for every entry in expressList

	@return:    nothing
	"""
	logging.debug("data before update from expressList: %s", data)
	for i, exList in enumerate(expressList):
		#update with eapoc_id (RIC)
		data['ric'] =  exList[i][1]
		#update with eapoc_sub (Sub RIC)
		data['function'] = exList[i][2]
		# Add function as character a-d to dataset (reused from includes/poc.py)
		data["functionChar"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
		#update with eapoc_id (RIC)
		data['description'] = exList[i][1]
		logging.debug("data after update from expressList: %s", data)
		try:
			from includes import alarmHandler
			alarmHandler.processAlarmHandler(typ, freq, data)
		except:
			logging.error("processing alarm failed")
			logging.debug("processing alarm failed", exc_info=True)
