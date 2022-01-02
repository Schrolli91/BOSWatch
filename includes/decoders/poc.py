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

from includes import globalVars  # Global variables
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

	@return:    Checks both allow/deny-rule and filter-range (suitable for signal-RIC)
	@exception: none
	"""

	allowed = 0
	has_geo = False

	# 1.) If allowed RICs is set, only they will path,
	#       If RIC is the right one return True, else False
	if globalVars.config.get("POC", "allow_ric"):
		if poc_id in globalVars.config.get("POC", "allow_ric"):
			logging.info("RIC %s is allowed", poc_id)
			return True
		else:
			logging.info("RIC %s is not in the allowed list", poc_id)
			allowed = 0
	# 2.) If denied RIC, return False
	if poc_id in globalVars.config.get("POC", "deny_ric"):
		logging.info("RIC %s is denied by config.ini", poc_id)
		return False # RIC is denied - strongest way to block
	# 3.) Check Range, return False if outside def. range
	if globalVars.config.getint("POC", "filter_range_start") < int(poc_id) < globalVars.config.getint("POC", "filter_range_end"):
		logging.info("RIC %s in between filter range", poc_id)
		return True
	else:
		logging.info("RIC %s out of filter range", poc_id)
		allowed = 0
	# 4.) Implementation for net identifiers
	if globalVars.config.get("POC", "netIdent_ric"):
		if poc_id in globalVars.config.get("POC", "netIdent_ric"):
			logging.info("RIC %s as net identifier", poc_id)
			return True
		else:
			allowed = 0
	# 5.) Implementation for multicastAlarm
	if globalVars.config.get("multicastAlarm", "multicastAlarm_delimiter_ric"):
		if poc_id in globalVars.config.get("multicastAlarm", "multicastAlarm_delimiter_ric"):
			logging.info("RIC %s as multicastAlarm delimiter", poc_id)
			return True
		else:
			allowed = 0
	if globalVars.config.get("multicastAlarm", "multicastAlarm_ric"):
		if poc_id in globalVars.config.get("multicastAlarm", "multicastAlarm_ric"):
			logging.info("RIC %s as multicastAlarm message", poc_id)
			return True
		else:
			allowed = 0

	if allowed == 0:
		return False
	return True
##
#
# POCSAG decoder function
# validate -> check double alarm -> log
#
def decode(freq, decoded):
	"""
	Export POCSAG information from Multimon-NG string and call alarmHandler.processAlarmHandler()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini

	@return:    nothing
	@exception: Exception if POCSAG decode failed
	"""
	has_geo = False
	
	try:
		bitrate = 0

		if "POCSAG512:" in decoded:
			bitrate = 512
			poc_id = decoded[20:27].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[39])+1)

		elif "POCSAG1200:" in decoded:
			bitrate = 1200
			poc_id = decoded[23:30].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[42])+1)

		elif "POCSAG2400:" in decoded:
			bitrate = 2400
			poc_id = decoded[23:30].replace(" ", "").zfill(7)
			poc_sub = str(int(decoded[42])+1)

		if bitrate == 0:
			logging.warning("POCSAG Bitrate not found")
			logging.debug(" - (%s)", decoded)
		else:
			logging.debug("POCSAG Bitrate: %s", bitrate)

			if "Alpha:" in decoded: #check if there is a text message
				poc_text = decoded.split('Alpha:   ')[1].strip().replace('<NUL><NUL>','').replace('<NUL>','').replace('<NUL','').replace('< NUL>','').replace('<EOT>','').strip()
				if globalVars.config.getint("POC","geo_enable"):
					try:
						logging.debug("Using %s to find geo-tag in %s", globalVars.config.get("POC","geo_format"),poc_text)
						m = re.search(globalVars.config.get("POC","geo_format"),poc_text)
						if m:
							logging.debug("Found geo-tag in message, parsing...")
							has_geo = True
							geo_order = globalVars.config.get("POC","geo_order").split(',')
							if geo_order[0].lower == "lon":
								lat = m.group(1) + "." + m.group(2)
								lon = m.group(3) + "." + m.group(4)
							else:
								lon = m.group(1) + "." + m.group(2)
								lat = m.group(3) + "." + m.group(4)
								logging.debug("Finished parsing geo; lon: %s, lat: %s", lon, lat)
						else:
							logging.debug("No geo-tag found")
							has_geo = False
					except:
						has_geo = False
						logging.error("Exception parsing geo-information",exc_info=true)
				else:
					has_geo = False
			else:
				poc_text = ""
			if re.search("[0-9]{7}", poc_id) and re.search("[1-4]{1}", poc_sub): #if POC is valid
				if isAllowed(poc_id):

					# check for double alarm
					if doubleFilter.checkID("POC", poc_id+poc_sub, poc_text):
						data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate, "description":poc_id, "has_geo":has_geo}
						if has_geo == True:
							data["lon"] = lon
							data["lat"] = lat
						# Add function as character a-d to dataset
						data["functionChar"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
						data["ricFuncChar"] = data["ric"] + data["functionChar"]

						logging.info("POCSAG%s: %s %s %s ", data["bitrate"], data["ric"], data["function"], data["msg"])

						# If enabled, look up description
						if globalVars.config.getint("POC", "idDescribed"):
							from includes import descriptionList
							data["description"] = descriptionList.getDescription("POC", data["ric"]+data["functionChar"])

						# multicastAlarm processing if enabled and a message without text or delimiter RIC or netIdent_ric received
						if globalVars.config.getint("multicastAlarm", "multicastAlarm") and data["ric"] != globalVars.config.get("POC", "netIdent_ric") and (data["msg"] == "" or data["ric"] in globalVars.config.get("multicastAlarm", "multicastAlarm_delimiter_ric")):
							logging.debug(" - multicastAlarm without msg")
							from includes import multicastAlarm
							multicastAlarm.newEntrymultiList(data)

						# multicastAlarm processing if enabled and alarm message has been received
						elif globalVars.config.getint("multicastAlarm", "multicastAlarm") and data["msg"] != "" and data["ric"] in globalVars.config.get("multicastAlarm", "multicastAlarm_ric"):
							logging.debug(" - multicastAlarm with message")
							from includes import multicastAlarm
							multicastAlarm.multicastAlarmExec(freq, data)

						else:
							# processing the alarm
							try:
								from includes import alarmHandler
								alarmHandler.processAlarmHandler("POC", freq, data)
							except:
								logging.error("processing alarm failed")
								logging.debug("processing alarm failed", exc_info=True)
					# in every time save old data for double alarm
					doubleFilter.newEntry(poc_id+poc_sub, poc_text)
				else:
					logging.debug("POCSAG%s: %s is not allowed", bitrate, poc_id)
			else:
				logging.warning("No valid POCSAG%s RIC: %s SUB: %s", bitrate, poc_id, poc_sub)
	except:
		logging.error("error while decoding")
		logging.debug("error while decoding", exc_info=True)
