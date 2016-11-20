#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
ZVEI Decoder

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import re      # Regex for validation

from includes import globalVars  # Global variables
from includes import doubleFilter  # double alarm filter

##
#
# Local function to remove the 'F'
#
def removeF(zvei):
	"""
	Resolve the F from the repeat Tone

	@type    zvei: string
	@param   zvei: ZVEI Information

	@return:    ZVEI without F
	@exception: none
	"""
	if "F" in zvei:
		zvei_old = zvei
		for i in range(1, len(zvei_old)):
			if zvei[i] == "F":
				zvei = zvei.replace("F",zvei[i-1],1)
		logging.debug("resolve F: %s -> %s", zvei_old, zvei)
	return zvei

##
#
# ZVEI decoder function
# validate -> check double alarm -> log
#
def decode(freq, decoded):
	"""
	Export ZVEI Information from Multimon-NG RAW String and call alarmHandler.processAlarmHandler()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini

	@return:    nothing
	@exception: Exception if ZVEI decode failed
	"""
	try:
		zvei_id = decoded[7:12]    # ZVEI Code
		zvei_id = removeF(zvei_id) # resolve F
		if re.search("[0-9]{5}", zvei_id): # if ZVEI is valid
			# check for double alarm
			if doubleFilter.checkID("ZVEI", zvei_id):
				logging.info("5-Ton: %s", zvei_id)
				data = {"zvei":zvei_id, "description":zvei_id}
				# If enabled, look up description
				if globalVars.config.getint("ZVEI", "idDescribed"):
					from includes import descriptionList
					data["description"] = descriptionList.getDescription("ZVEI", zvei_id)
				# processing the alarm
				try:
					from includes import alarmHandler
					alarmHandler.processAlarmHandler("ZVEI", freq, data)
				except:
					logging.error("processing alarm failed")
					logging.debug("processing alarm failed", exc_info=True)
			# in every time save old data for double alarm
			doubleFilter.newEntry(zvei_id)
		else:
			logging.warning("No valid ZVEI: %s", zvei_id)
	except:
		logging.error("error while decoding")
		logging.debug("error while decoding", exc_info=True)
