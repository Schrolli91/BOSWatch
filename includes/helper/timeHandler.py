#!/usr/bin/python
# -*- coding: cp1252 -*-
#

"""
little Helper to get easy the curent date or time
for direct use in plugins to save code

@author: Bastian Schroll
"""

import logging

import time


def curtime(format="%d.%m.%Y %H:%M:%S"):
	"""
	Returns formated date and/or time
	see: https://docs.python.org/2/library/time.html#time.strftime

	@type    format: string
	@param   format: Python time Format-String

	@return:    Formated Time and/or Date
	@exception: Exception if Error in format
	"""
	try:
		return time.strftime(format)
	except:
		logging.warning("error in time-format-string")
		logging.debug("error in time-format-string", exc_info=True)


def getDate():
	"""
	Returns the date

	@return: Formated date
	"""
	return curtime("%d.%m.%Y")

def getTime():
	"""
	Returns the time

	@return: Formated time
	"""
	return curtime("%H:%M:%S")

def getTimestamp():
	"""
	Returns a integer timestamp

	@return: integer timestamp
	"""
	return int(time.time())
