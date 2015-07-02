#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
doubleFilter is the central function to filter out double alarms.
You can set the number of historical entries the filter will check
and the time ignoring the id in case of a double alarm

@author: Jens Herrmann

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import time    # timestamp for doublealarm

from includes import globals  # Global variables

#
# ListStructure [0..n] = (ID, TimeStamp, msg)
#

def checkID(typ, id, msg=""):
	"""
	check if id was called in the last x sec and n entries

	@requires:  Configuration has to be set in the config.ini

	@return:    True if check was OK
	@return:    False if double was found
	"""
	timestamp = int(time.time()) # Get Timestamp

	for i in range(len(globals.doubleList)):
		(xID, xTimestamp, xMsg) = globals.doubleList[i]
		# given ID found?
		# return False if the first entry in double_ignore_time is found, we will not check for younger ones...
		if id == xID and timestamp < xTimestamp + globals.config.getint("BOSWatch", "doubleFilter_ignore_time"):
			# if wanted, we have to check the msg additional
			if "POC" in typ and globals.config.getint("BOSWatch", "doubleFilter_check_msg"):
				# if msg is a substring of xMsg we found a double
				if msg in xMsg:
					logging.info("%s double alarm (id+msg): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
					return False
			else:
				logging.info("%s double alarm (id): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
				return False
	return True


def newEntry(id, msg = ""):
	"""
	new entry in double alarm list

	@return:    nothing
	"""
	timestamp = int(time.time()) # Get Timestamp
	globals.doubleList.append((id, timestamp, msg))

	logging.debug("Added %s to doubleList", id)

	# now check if list has more than n entries:
	if len(globals.doubleList) > globals.config.getint("BOSWatch", "doubleFilter_ignore_entries"):
		# we have to kill the oldest one
		globals.doubleList.pop(0)
