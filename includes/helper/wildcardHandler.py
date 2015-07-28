#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
little Helper to replace fast and easy the standard wildcards
for direct use in plugins to save code

@author: Bastian Schroll
@author: Jens Herrmann
"""

import logging

from includes.helper import timeHandler


def replaceWildcards(text, data, lineBrakeAllowed=False):
	"""
	Replace all official Wildcards with the Information from the data[] var

	@type    text: string
	@param   text: Input text with wildcards
	@type    data: map
	@param   data: map of data (structure see interface.txt)
	@type    lineBrakeAllowed: Boolean
	@param   lineBrakeAllowed: switch to allow lineBreak (%BR%) as wildcard

	@return:    text with replaced wildcards
	@exception: Exception if Error at replace
	"""
	try:
		# replace date and time wildcards
		text = text.replace("%TIME%", timeHandler.getTime()).replace("%DATE%", timeHandler.getDate())
		
		# replace some special chars
		if lineBrakeAllowed == True:
			text = text.replace("%BR%", "\r\n")
		text = text.replace("%LPAR%", "(")
		text = text.replace("%RPAR%", ")")

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

		logging.debug("wildcards been replaced")

		return text

	except:
		logging.warning("error in wildcard replacement")
		logging.debug("error in wildcard replacement", exc_info=True)
