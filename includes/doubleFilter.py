#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
doubleFilter is the central function to filter out double alarms.
You can set the number of historical entries the filter will check
and the time ignoring the id in case of a double alarm

@author: Jens Herrmann

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import time    # timestamp for doublealarm

from includes import globalVars  # Global variables

#
# ListStructure [0..n] = (Data, TimeStamp, msg)
#
doubleList = []


def checkID(typ, data, msg=""):
	"""
	check if id was called in the last x sec and n entries

	@requires:  Configuration has to be set in the config.ini

	@return:    True if check was OK
	@return:    False if double was found
	"""
	timestamp = int(time.time()) # Get Timestamp

	logging.debug("checkID: %s (%s)", data, msg)
	for (xID, xTimestamp, xMsg) in doubleList:
		# given ID found?
		# return False if the first entry in double_ignore_time is found, we will not check for younger ones...
		if data == xID and timestamp < xTimestamp + globalVars.config.getint("BOSWatch", "doubleFilter_ignore_time"):
			logging.debug("-- previous id %s is within doubleFilter_ignore_time (%ss)", xID, globalVars.config.getint("BOSWatch", "doubleFilter_ignore_time"))
			# if wanted, we have to check the msg additional
			if "POC" in typ and globalVars.config.getint("BOSWatch", "doubleFilter_check_msg"):
				logging.debug("-- compare msg:")
				logging.debug("---- current msg: (%s)", msg.strip())
				logging.debug("---- previous msg: (%s)", xMsg)
				# if msg is a substring of xMsg we found a double
				if msg.strip() in xMsg:
					logging.info("%s double alarm (id+msg): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
					return False
			else:
				logging.info("%s double alarm (id): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
				return False
	return True


def newEntry(data, msg = ""):
	"""
	new entry in double alarm list

	@return:    nothing
	"""
	global doubleList
	timestamp = int(time.time()) # Get Timestamp
	doubleList.append((data, timestamp, msg.strip()))

	logging.debug("Added %s to doubleList", data)

	# now check if list has more than n entries:
	if len(doubleList) > globalVars.config.getint("BOSWatch", "doubleFilter_ignore_entries"):
		# we have to kill the oldest one
		doubleList.pop(0)
