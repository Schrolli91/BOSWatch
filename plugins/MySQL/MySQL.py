#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger

import mysql
import mysql.connector

from includes import globals  # Global variables


def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("MySQL"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
				
		try:
			logging.debug("connect to MySQL")
			connection = mysql.connector.connect(host = globals.config.get("MySQL","dbserver"), user = globals.config.get("MySQL","dbuser"), passwd = globals.config.get("MySQL","dbpassword"), db = globals.config.get("MySQL","database"))
			cursor = connection.cursor()
		except:
			logging.exception("cannot connect to MySQL")
		else:
			
			try:
				logging.debug("Insert %s", typ)
				
				if typ == "FMS":
					#data = {"fms":fms_id[0:8], "status":fms_status, "direction":fms_direction, "tsi":fms_tsi}
					cursor.execute("INSERT INTO "+globals.config.get("MySQL","tableFMS")+" (time,fms,status,direction,tsi) VALUES (NOW(),%s,%s,%s,%s)",(data["fms"],data["status"],data["direction"],data["tsi"]))
					
				elif typ == "ZVEI":
					#data = {"zvei":zvei_id}
					cursor.execute("INSERT INTO "+globals.config.get("MySQL","tableZVEI")+" (time,zvei) VALUES (NOW(),%s)",(data["zvei"]))
					
				elif typ == "POC":
					#data = {"ric":poc_id, "function":poc_sub, "msg":poc_text}
					cursor.execute("INSERT INTO "+globals.config.get("MySQL","tablePOC")+" (time,ric,funktion,text) VALUES (NOW(),%s,%s,%s)",(data["ric"],data["function"],data["msg"]))
					
				else:
					logging.warning("Invalid Typ: %s", typ)	
			except:
				logging.exception("cannot Insert %s", typ)
					 
		finally:
			logging.debug("close MySQL")
			cursor.close()
			connection.close() #Close connection in every case  
	except:
		logging.exception("unknown error")