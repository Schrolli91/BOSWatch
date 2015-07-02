#!/usr/bin/python
# -*- coding: cp1252 -*-
#

"""
little Helper functions
mainly for direct use in plugins to save code

@author: 		Bastian Schroll
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


def replaceWildcards(text,data):
	"""
	Replace all official Wildcards with the Information from the data[] var

	@type    text: string
	@param   text: Input text with wildcards
	@type    data: map
	@param   data: map of data (structure see interface.txt)

	@return:    text with replaced wildcards
	@exception: Exception if Error at replace
	"""
	try:
		# replace date and time wildcards
		text = text.replace("%TIME%", curtime("%H:%M:%S")).replace("%DATE%", curtime("%d.%m.%Y"))

		# replace FMS data
		if "fms" in data: text = text.replace("%FMS%", data["fms"])
		if "status" in data: text = text.replace("%STATUS%", data["status"])
		if "direction" in data: text = text.replace("%DIR%", data["direction"])
		if "directionText" in data: text = text.replace("%DIRT%", data["directionText"])
		if "tsi" in data: text = text.replace("%TSI%", data["tsi"])

		# replace ZVEI data
		if "zvei" in data: text = text.replace("%ZVEI%", data["zvei"])

		# replace POC data
		if "ric" in data: text = text.replace("%RIC%", data["ric"])
		if "function" in data: text = text.replace("%FUNC%", data["function"])
		if "functionChar" in data: text = text.replace("%FUNCCHAR%", data["functionChar"])
		if "msg" in data: text = text.replace("%MSG%", data["msg"])
		if "bitrate" in data: text = text.replace("%BITRATE%", str(data["bitrate"]))

		# replace description (exists by all)
		if "description" in data: text = text.replace("%DESCR%", data["description"])

		return text

	except:
		logging.warning("error wildcard replacement")
		logging.debug("error wildcard replacement", exc_info=True)
