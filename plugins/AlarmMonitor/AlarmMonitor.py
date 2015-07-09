#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
PLATZHALTER
"""

import logging # Global logger
import fileinput, sys, os

from includes import globals  # Global variables
from time import *
#
#
#AlarmMonitor Plugin to show Alarmtext on a TV for x Minutes.
#
def run(typ,freq,data):
	"""
	Dieses Modul wird zum Aussenden einer Befehlskette für ein Alarmmonitor benötigt
	"""
	try:
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("AlarmMonitor"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
	
		
		if typ == "FMS":
			logging.exception("FMS wird nicht unterstützt vom Alarmmonitor")
		elif typ == "ZVEI":
			logging.exception("ZVEI wird nicht unterstützt vom Alarmmonitor")
		elif typ == "POC":
			if globals.config.get("AlarmMonitor","RICFILTER") == "1" :
				logging.debug("RIC Filter aktiv") 
				RIC = data["ric"]
				RIC1 = globals.config.get("AlarmMonitor","RIC1")
				RIC2 = globals.config.get("AlarmMonitor","RIC2")
				RIC3 = globals.config.get("AlarmMonitor","RIC3")
				RIC4 = globals.config.get("AlarmMonitor","RIC4")
				RIC5 = globals.config.get("AlarmMonitor","RIC5")
				
				if (RIC1 == data["ric"]) or (RIC2 == data["ric"]) or (RIC3 == data["ric"]) or (RIC4 == data["ric"]) or (RIC5 == data["ric"]):
					logging.debug("Filter hat RIC: %s erkannt, beginne mit Alarm",data["ric"])

					nowfilter = 1
				else:
					logging.debug("Alarmfilter aktiv, RIC: %s gefiltert",data["ric"])
					nowfilter = 0
			else:
				logging.debug("RIC Filer nicht aktiv")
				nowfilter = 1
			
			if nowfilter == 1:
				try:
					logging.debug("Open Alarm.html")
					alarmzeit = time()
					alarm = open("plugins/AlarmMonitor/"+globals.config.get("AlarmMonitor","alarm_src")).readlines()
					index = open("plugins/AlarmMonitor/"+globals.config.get("AlarmMonitor","html_dest"),"w+")
				except:
					logging.error("Cant open Alarmfile")
				
				TIME = strftime("%H:%M",localtime())				
				message = data["msg"]
				message.replace("/","<br>")
				for line in alarm:
				
				# INDEX / wird überschrieben .... erst Meldung in html formatieren
				
					index.write(line.replace("%MELDUNG%",message).replace("%UHRZEIT%",TIME))
					
				index.close()


				if globals.config.get("AlarmMonitor","screen_ctrl") == "1":
					logging.debug("Starte Bildschirm")
					os.system("export DISPLAY=:0.0")
					os.system("xhost +")
					os.system("Chrome-Refresh")
					os.system("tvservice -p")
					os.system("chvt 6")
					os.system("chvt 7")	
					os.system("aplay plugins/AlarmMonitor/bmd_ton1.wav")
					os.system("aplay plugins/AlarmMonitor/bmd_ton1.wav")
					os.system("aplay plugins/AlarmMonitor/bmd_ton1.wav")
					# Übergebe Alarmzeit und 2x Auszeit + Pfad zu Uhr an externes Programm		
					# subprocess.Popen([])	
					sc = open("plugins/AlarmMonitor/time_data.txt","w+")
					sc.write("[settings]\n")
					sc.write("t_monitor = "+globals.config.get("AlarmMonitor","t_monitor")+"\n")
					sc.write("t_lights = "+globals.config.get("AlarmMonitor","t_lights")+"\n")
					sc.write("ss_src = "+globals.config.get("AlarmMonitor","ss_src")+"\n")
					sc.write("html_dest = "+globals.config.get("AlarmMonitor","html_dest")+"\n")
					sc.write("[alarm]\n")
					#sc.write( TIME NOW!!!)
					sc.close()
					
			else:
				logging.warning("Wrong Typ")

			
	except:
		logging.exception("unknown error")