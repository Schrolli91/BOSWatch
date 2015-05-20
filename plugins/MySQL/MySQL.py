#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables
import mysql
import mysql.connector

def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("MySQL"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
			
		#open DB-Connection
		try:
			connection = mysql.connector.connect(host = globals.config.get("MySQL","dbserver"), user = globals.config.get("MySQL","dbuser"), passwd = globals.config.get("MySQL","dbpassword"), db = globals.config.get("MySQL","database"))
			cursor = connection.cursor()
	
			if typ == "FMS":
				#data = {"fms":fms_id[0:8], "status":fms_status, "direction":fms_direction, "tsi":fms_tsi}
				cursor.execute("INSERT INTO "+globals.config.get("MySQL","tableFMS")+" (time,fms,status,direction,tsi) VALUES (NOW(),%s,%s,%s,%s)",(data["fms"],data["status"],data["direction"],data["tsi"]))

			elif typ == "ZVEI":
				#data = {"zvei":zvei_id}
				cursor.execute("INSERT INTO "+globals.config.get("MySQL","tableZVEI")+" (time,zvei) VALUES (NOW(),"+data["zvei"]+")")

			elif typ == "POC":
				#data = {"ric":poc_id, "function":poc_sub, "msg":poc_text}
				cursor.execute("INSERT INTO "+globals.config.get("MySQL","tablePOC")+" (time,ric,funktion,text) VALUES (NOW(),%s,%s,%s)",(data["ric"],data["function"],data["msg"]))

			else:
				logging.warning(typ + " not supportet")
				return

			cursor.close()
			connection.commit()
		except:
			logging.exception("%s to MySQL failed", typ)  
		finally:
			connection.close() #Close connection in every case  
	except:
		logging.exception("unknown error")