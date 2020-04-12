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

from includes import globalVars

from includes.helper import timeHandler


def replaceWildcards(text, data):
	"""
	Replace all official Wildcards with the Information from the data[] var

	@type    text: string
	@param   text: Input text with wildcards
	@type    data: map
	@param   data: map of data (structure see readme.md in plugin folder)

	@return:    text with replaced wildcards
	@exception: Exception if Error at replace
	"""
	try:
		# replace date and time wildcards
		text = text.replace("%TIME%", timeHandler.getTime(data["timestamp"])).replace("%DATE%", timeHandler.getDate(data["timestamp"]))

		# replace some special chars
		text = text.replace("%BR%", "\r\n")
		text = text.replace("%LPAR%", "(")
		text = text.replace("%RPAR%", ")")
		text = text.replace("%BTA%", "<b>")
		text = text.replace("%BTE%", "</b>")
		text = text.replace("%ITA%", "<i>")
		text = text.replace("%ITE%", "</i>")
		text = text.replace("%UTA%", "<u>")
		text = text.replace("%UTE%", "</u>")

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
		if "function" in data:
			text = text.replace("%FUNC%", data["function"])
			if data["function"] == "1": text = text.replace("%FUNCTEXT%", globalVars.config.get("POC","rica"))
			if data["function"] == "2": text = text.replace("%FUNCTEXT%", globalVars.config.get("POC","ricb"))
			if data["function"] == "3": text = text.replace("%FUNCTEXT%", globalVars.config.get("POC","ricc"))
			if data["function"] == "4": text = text.replace("%FUNCTEXT%", globalVars.config.get("POC","ricd"))
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
