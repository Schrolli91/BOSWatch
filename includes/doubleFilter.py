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
# ListStructure [0..n] = (ID, TimeStamp)
#

def checkID(typ, id):
	"""
	check if id was called in the last x sec and n entries
	
	@requires:  Configuration has to be set in the config.ini
	
	@return:    True if check was OK
	@return:    False if double was found
	"""
	timestamp = int(time.time()) # Get Timestamp 

	for i in range(len(globals.doubleList)):
		(xID, xTimestamp) = globals.doubleList[i]
		# given ID found?
		# return False if the first entry in double_ignore_time is found, we will not check for younger ones...
		if id == xID and timestamp < xTimestamp + globals.config.getint("BOSWatch", "double_ignore_time"):
			logging.info("%s double alarm: %s within %s second(s)", typ, xID, timestamp-xTimestamp)
			return False
	return True
	

def newEntry(id):
	"""
	new entry in double alarm list
	
	@return:    nothing
	"""
	timestamp = int(time.time()) # Get Timestamp 
	globals.doubleList.append((id, timestamp))
	
	# now check if list has more than n entries:
	if len(globals.doubleList) > globals.config.getint("BOSWatch", "double_ignore_entries"):
		# we have to kill the oldest one
		globals.doubleList.pop(0)	