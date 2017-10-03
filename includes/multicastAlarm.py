#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
multicastAlarm is the function to enable BOSwatch to work in networks that optimise the transmission of POCSAG telegrams

@author: Fabian Kessler

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import time    # timestamp for multicastAlarm

from includes import globalVars  # Global variables

#
# ListStructure [0..n] = (Data, TimeStamp)
#
multiList = []

def newEntrymultiList(data):
	"""
	add entry to multi alarm list and remove old entries

	@return:    nothing
	"""
	timestamp = int(time.time())
	# multicastAlarm processing if enabled and delimiter RIC has been received
	if data['ric'] == globalVars.config.get("multicastAlarm", "multicastAlarm_delimiter_ric"):
		multiList = []
		logging.debug("multicastAlarm delimiter RIC received --> buffer cleared")
	else:
		multiList.append([data, timestamp])
		logging.debug("Added %s to multiList", data['ric'])
		# check for old entries in multiList
		for (xData, xTimestamp) in multiList:
			if xTimestamp > timestamp-globalVars.config.getint("multicastAlarm", "multicastAlarm_ignore_time"):
				multiList.remove([xData, xTimestamp])


def multicastAlarmExec(freq, data):
	"""
	call alarmHandler for every entry in multiList

	@return:    nothing
	"""
	logging.debug("data before update from multiList: %s", data)
	for (xData, xTimestamp) in multiList:
		#update data with values multiList
		data['ric'] =  xData['ric']
		data['function'] = xData['ric']
		data['functionChar'] = xData['ric']
		data['description'] = xData['ric']
		logging.debug("data after update from multiList: %s", data)
		try:
			from includes import alarmHandler
			alarmHandler.processAlarmHandler("POC", freq, data)
		except:
			logging.error("processing alarm failed")
			logging.debug("processing alarm failed", exc_info=True)
