if "ZVEI2:" in decoded:
	logging.debug("recieved ZVEI")			
	
	zvei_id = decoded[7:12] #ZVEI Code  
	if re.search("[0-9F]{5}", zvei_id): #if ZVEI is valid
		if zvei_id == zvei_id_old and timestamp < zvei_time_old + int(config["zvei_double_ignore_time"]): #check for double alarm
			logging.warning("ZVEI double alarm: %s within %s second(s)", zvei_id_old, timestamp-zvei_time_old)
			zvei_time_old = timestamp #in case of double alarm, zvei_double_ignore_time set new
		else:
			logging.info("5-Ton: %s", zvei_id)
			data = {"zvei":zvei_id}
			throwAlarm("ZVEI",data)

			zvei_id_old = zvei_id #save last id
			zvei_time_old = timestamp #save last time
	else:
		logging.warning("No valid ZVEI: %s", zvei_id)