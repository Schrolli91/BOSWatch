#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import time #timestamp for doublealarm
import re #Regex for validation

from includes import globals  # Global variables
from includes import pluginloader


def decode(decoded):
	timestamp = int(time.time())#Get Timestamp                  
		
	#FMS Decoder Section    
	#check FMS: -> check CRC -> validate -> check double alarm -> log
	if "FMS:" in decoded:   
		logging.debug("recieved FMS")
			
		fms_service = decoded[19]       #Organisation
		fms_country = decoded[36]       #Bundesland
		fms_location = decoded[65:67]   #Ort
		fms_vehicle = decoded[72:76]    #Fahrzeug
		fms_status = decoded[84]        #Status
		fms_direction = decoded[101]    #Richtung
		fms_tsi = decoded[114:117]      #Taktische Kruzinformation
			
		if "CRC correct" in decoded: #check CRC is correct  
			fms_id = fms_service+fms_country+fms_location+fms_vehicle+fms_status+fms_direction #build FMS id
			if re.search("[0-9a-f]{8}[0-9a-f]{1}[01]{1}", fms_id): #if FMS is valid
				if fms_id == globals.fms_id_old and timestamp < globals.fms_time_old + globals.config.getint("BOSWatch", "fms_double_ignore_time"): #check for double alarm
					logging.info("FMS double alarm: %s within %s second(s)", globals.fms_id_old, timestamp-globals.fms_time_old)
					globals.fms_time_old = timestamp #in case of double alarm, fms_double_ignore_time set new
				else:
					logging.info("FMS:%s Status:%s Richtung:%s TKI:%s", fms_id[0:8], fms_status, fms_direction, fms_tsi)
					data = {"fms":fms_id[0:8], "status":fms_status, "direction":fms_direction, "tsi":fms_tsi}
					from includes import pluginHandler
					pluginHandler.throwAlarm("FMS",data)
					
					globals.fms_id_old = fms_id #save last id
					globals.fms_time_old = timestamp #save last time	
			else:
				logging.warning("No valid FMS: %s", fms_id)    
		else:
			logging.warning("FMS CRC incorrect")
				

	#ZVEI Decoder Section
	#check ZVEI: -> validate -> check double alarm -> log     
	if "ZVEI2:" in decoded:
		logging.debug("recieved ZVEI")			
		
		zvei_id = decoded[7:12] #ZVEI Code  
		if re.search("[0-9F]{5}", zvei_id): #if ZVEI is valid
			if zvei_id == globals.zvei_id_old and timestamp < globals.zvei_time_old + globals.config.getint("BOSWatch", "zvei_double_ignore_time"): #check for double alarm
				logging.info("ZVEI double alarm: %s within %s second(s)", globals.zvei_id_old, timestamp-globals.zvei_time_old)
				globals.zvei_time_old = timestamp #in case of double alarm, zvei_double_ignore_time set new
			else:
				logging.info("5-Ton: %s", zvei_id)
				data = {"zvei":zvei_id}
				from includes import pluginHandler
				pluginHandler.throwAlarm("ZVEI",data)

				globals.zvei_id_old = zvei_id #save last id
				globals.zvei_time_old = timestamp #save last time
		else:
			logging.warning("No valid ZVEI: %s", zvei_id)
		
		
	#POCSAG Decoder Section
	#check POCSAG -> validate -> check double alarm -> log      
	if "POCSAG" in decoded:
		logging.debug("recieved POCSAG")				
		bitrate = 0
		
		if "POCSAG512:" in decoded:
			bitrate = 512
			poc_id = decoded[20:27]
			poc_sub = decoded[39].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
			
		elif "POCSAG1200:" in decoded:
			bitrate = 1200
			poc_id = decoded[21:28]
			poc_sub = decoded[40].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
			
		elif "POCSAG2400:" in decoded:
			bitrate = 2400
			poc_id = decoded[21:28]
			poc_sub = decoded[40].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
				
		if bitrate is 0:
			logging.warning("POCSAG Bitrate not found")
		else:
			logging.debug("POCSAG Bitrate: %s", bitrate)
		
			if "Alpha:" in decoded: #check if there is a text message
				poc_text = decoded.split('Alpha:   ')[1].strip().rstrip('<EOT>').strip()
			else:
				poc_text = ""
			
			if re.search("[0-9]{7}", poc_id): #if POC is valid
				if int(poc_id) >= globals.config.getint("BOSWatch", "poc_filter_range_start"):
					if int(poc_id) <= globals.config.getint("BOSWatch", "poc_filter_range_end"):
						if poc_id == globals.poc_id_old and timestamp < globals.poc_time_old + globals.config.getint("BOSWatch", "poc_double_ignore_time"): #check for double alarm
							logging.info("POCSAG%s double alarm: %s within %s second(s)", bitrate, globals.poc_id_old, timestamp-globals.poc_time_old)
							globals.poc_time_old = timestamp #in case of double alarm, poc_double_ignore_time set new
						else:
							logging.info("POCSAG%s: %s %s %s ", bitrate, poc_id, poc_sub, poc_text)
							data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate}
							from includes import pluginHandler
							pluginHandler.throwAlarm("POC",data)
			
							globals.poc_id_old = poc_id #save last id
							globals.poc_time_old = timestamp #save last time		
					else:
						logging.info("POCSAG%s: %s out of filter range (high)", bitrate, poc_id)
				else:
					logging.info("POCSAG%s: %s out of filter range (low)", bitrate, poc_id)
			else:
				logging.warning("No valid POCSAG%s RIC: %s", bitrate, poc_id)