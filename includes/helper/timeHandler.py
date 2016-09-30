#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
little Helper to get easy the curent date or time
for direct use in plugins to save code

@author: Bastian Schroll
@author: Jens Herrmann
"""

import logging

import time


def curtime(format="%d.%m.%Y %H:%M:%S", timestamp=""):
	"""
	Returns formated date and/or time
	see: https://docs.python.org/2/library/time.html#time.strftime

	@type    format: string
	@param   format: Python time Format-String
	@type    timestamp: floating point number
	@param   timestamp: time in seconds since the epoch

	@return:    Formated Time and/or Date
	@exception: Exception if Error in format
	"""
	try:
		if timestamp == "":
			return time.strftime(format)
		else:
			return time.strftime(format, time.localtime(timestamp))
	except:
		logging.warning("error in time-format-string")
		logging.debug("error in time-format-string", exc_info=True)


def getDateTime(timestamp=""):
	"""
	Returns the date and time

	@return: Formated date
	"""
	return curtime("%d.%m.%Y %H:%M:%S", timestamp)


def getDate(timestamp=""):
	"""
	Returns the date

	@return: Formated date
	"""
	return curtime("%d.%m.%Y", timestamp)


def getTime(timestamp=""):
	"""
	Returns the time

	@return: Formated time
	"""
	return curtime("%H:%M:%S", timestamp)


def getTimestamp():
	"""
	Returns a integer timestamp

	@return: integer timestamp
	"""
	return int(time.time())
