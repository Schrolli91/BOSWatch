#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
POCSAG Decoder

@author: Bastian Schroll
@author: Jens Herrmann

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import re      # Regex for validation

from includes import globals  # Global variables
from includes import doubleFilter  # double alarm filter

##
#
# Simple local filter
#
def isAllowed(poc_id):
	"""
	Simple Filter Functions (Allowed, Denied and Range)

	@type    poc_id: string
	@param   poc_id: POCSAG Ric

	@requires:  Configuration has to be set in the config.ini

	@return:    True if the Ric is allowed, other False
	@exception: none
	"""
	# 1.) If allowed RICs is set, only they will path,
	#       If RIC is the right one return True, else False
	if globals.config.get("POC", "allow_ric"):
		if poc_id in globals.config.get("POC", "allow_ric"):
			logging.info("RIC %s is allowed", poc_id)
			return True
		else:
			logging.info("RIC %s is not in the allowed list", poc_id)
			return False
	# 2.) If denied RIC, return False
	elif poc_id in globals.config.get("POC", "deny_ric"):
		logging.info("RIC %s is denied by config.ini", poc_id)
		return False
	# 3.) Check Range, return False if outside def. range
	elif int(poc_id) < globals.config.getint("POC", "filter_range_start"):
		logging.info("RIC %s out of filter range (start)", poc_id)
		return False
	elif int(poc_id) > globals.config.getint("POC", "filter_range_end"):
		logging.info("RIC %s out of filter range (end)", poc_id)
		return False
	return True

##
#
# POCSAG decoder function
# validate -> check double alarm -> log
#
def decode(freq, decoded):
	"""
	Export POCSAG Information from Multimon-NG RAW String and call alarmHandler.processAlarmHandler()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini

	@return:    nothing
	@exception: Exception if POCSAG decode failed
	"""
	try:
		bitrate = 0

		if "POCSAG512:" in decoded:
			bitrate = 512
			poc_id = decoded[20:27].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[39])+1)

		elif "POCSAG1200:" in decoded:
			bitrate = 1200
			poc_id = decoded[21:28].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[40])+1)

		elif "POCSAG2400:" in decoded:
			bitrate = 2400
			poc_id = decoded[21:28].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[40])+1)

		if bitrate is 0:
			logging.warning("POCSAG Bitrate not found")
			logging.debug(" - (%s)", decoded)
		else:
			logging.debug("POCSAG Bitrate: %s", bitrate)

			if "Alpha:" in decoded: #check if there is a text message
				poc_text = decoded.split('Alpha:   ')[1].strip().rstrip('<EOT>').strip()
			else:
				poc_text = ""

			if re.search("[0-9]{7}", poc_id) and re.search("[1-4]{1}", poc_sub): #if POC is valid
				if isAllowed(poc_id):
					# check for double alarm
					if doubleFilter.checkID("POC", poc_id+poc_sub, poc_text):
						logging.info("POCSAG%s: %s %s %s ", bitrate, poc_id, poc_sub, poc_text)
						data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate, "description":poc_id}
						# Add function as character a-d to dataset
						data["functionChar"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
						# If enabled, look up description
						if globals.config.getint("POC", "idDescribed"):
							from includes import descriptionList
							data["description"] = descriptionList.getDescription("POC", poc_id)
						# processing the alarm
						try:
							from includes import alarmHandler
							alarmHandler.processAlarmHandler("POC", freq, data)
						except:
							logging.error("processing alarm failed")
							logging.debug("processing alarm failed", exc_info=True)
							pass
					# in every time save old data for double alarm
					doubleFilter.newEntry(poc_id+poc_sub, poc_text)
				else:
					logging.debug("POCSAG%s: %s is not allowed", bitrate, poc_id)
			else:
				logging.warning("No valid POCSAG%s RIC: %s SUB: %s", bitrate, poc_id, poc_sub)
	except:
		logging.error("error while decoding")
		logging.debug("error while decoding", exc_info=True)
