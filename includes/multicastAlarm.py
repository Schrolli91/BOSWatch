#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
multicastAlarm is the function to enable BOSwatch to deal networks that optimise the transmission of POCSAG telegrams

@author: Fabian Kessler

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import time    # timestamp for multicastAlarm

from includes import globalVars  # Global variables

multiList = []

def newEntrymultiList(eatyp, eapoc_id, eapoc_sub, eapoc_text):
	"""
	add entry to multi alarm list and remove old entries

	@return:    nothing
	"""
	global multiList
	tmpmultiList = []
	timestamp = int(time.time())
	# multicastAlarm processing if enabled and delimiter RIC has been received
	if eapoc_id == globalVars.config.get("multicastAlarm", "multicastAlarm_delimiter_ric"):
		multiList = []
		logging.debug("multicastAlarm delimiter RIC received --> buffer cleared  %s  %s %s ", eapoc_id, eapoc_sub, eapoc_text)
	else:
		multiList.append([eatyp, eapoc_id, eapoc_sub, eapoc_text.strip(), timestamp])
		logging.debug("Added %s  %s %s to multiList", eapoc_id, eapoc_sub, eapoc_text)
		# check for old entries in multiList
		for i in enumerate(multiList):
			# we have to remove entries older than timestamp - ignore time
			if int(multiList[i][4]) > timestamp-globalVars.config.getint("multicastAlarm", "multicastAlarm_ignore_time"):
				tmpmultiList.append(multiList[i])
	multiList = tmpmultiList


def multicastAlarmExec(typ, freq, data):
	"""
	call alarmHandler for every entry in multiList

	@return:    nothing
	"""
	logging.debug("data before update from multiList: %s", data)
	for i in enumerate(multiList):
		#update with eapoc_id (RIC)
		data['ric'] =  multiList[i][1]
		#update with eapoc_sub (Sub RIC)
		data['function'] = multiList[i][2]
		# Add function as character a-d to dataset (reused from includes/poc.py)
		data["functionChar"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
		#update with eapoc_id (RIC)
		data['description'] = multiList[i][1]
		logging.debug("data after update from multiList: %s", data)
		try:
			from includes import alarmHandler
			alarmHandler.processAlarmHandler(typ, freq, data)
		except:
			logging.error("processing alarm failed")
			logging.debug("processing alarm failed", exc_info=True)
