#!/usr/bin/python
# -*- coding: cp1252 -*-

##### Info #####
# BOSWatch
# Autor: Bastian Schroll
# Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG
# For more Information see the README.md
##### Info #####

import globals  # Global variables
import pluginloader

import logging

import argparse #for parse the args
import ConfigParser #for parse the config file
import re #Regex for validation
import os #for script path
import time #timestamp for doublealarm
import subprocess


def throwAlarm(typ,data):
	logging.debug("[  ALARM  ]")
	for name, plugin in pluginList.items():
		logging.debug("call Plugin: %s", name)
		plugin.run(typ,"0",data)
	logging.debug("[END ALARM]")
	
# Programm
try:
	try:
	
		#create logger
		globals.script_path = os.path.dirname(os.path.abspath(__file__))
		
		if not os.path.exists(globals.script_path+"/log/"):
			os.mkdir(globals.script_path+"/log/")
			
		#create new logger
		logger = logging.getLogger()
		logger.setLevel(logging.DEBUG)
		#set log string format
		formatter = logging.Formatter('%(asctime)s - %(module)-12s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
		#create a file logger
		fh = logging.FileHandler(globals.script_path+"/log/boswatch.log", "w")
		fh.setLevel(logging.DEBUG) #log level >= Debug
		fh.setFormatter(formatter)
		logger.addHandler(fh)
		#create a display logger
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO) #log level >= info
		ch.setFormatter(formatter)
		logger.addHandler(ch)
		
	except:
		logging.exception("cannot create logger")
	else:	
		try:
		
			#clear log
			bos_log = open(globals.script_path+"/log/boswatch.log", "w")
			rtl_log = open(globals.script_path+"/log/rtl_fm.log", "w")
			mon_log = open(globals.script_path+"/log/multimon.log", "w")
			bos_log.write("")
			rtl_log.write("")
			mon_log.write("")
			bos_log.close()
			rtl_log.close()
			mon_log.close()
			logging.debug("BOSWatch has started")
			logging.debug("Logfiles cleared")
			
		except:
			logging.exception("cannot clear Logfiles")	
		try:
		
			#parse args
			logging.debug("parse args")
			#With -h or --help you get the Args help
			#ArgsParser
			parser = argparse.ArgumentParser(prog="boswatch.py", description="BOSWatch is a Python Script to Recive and Decode German BOS Information with rtl_fm and multimon-NG", epilog="More Options you can find in the extern config.ini File in this Folder")
			#parser.add_argument("-c", "--channel", help="BOS Channel you want to listen")
			parser.add_argument("-f", "--freq", help="Frequency you want to listen", required=True)
			parser.add_argument("-d", "--device", help="Device you want to use (Check with rtl_test)", type=int, default=0)
			parser.add_argument("-e", "--error", help="Frequency-Error of your Device in PPM", type=int, default=0)
			parser.add_argument("-a", "--demod", help="Demodulation Functions", choices=['FMS', 'ZVEI', 'POC512', 'POC1200', 'POC2400'], required=True, nargs="+")
			parser.add_argument("-s", "--squelch", help="Level of Squelch", type=int, default=0)
			parser.add_argument("-v", "--verbose", help="Shows more Information", action="store_true")
			parser.add_argument("-q", "--quiet", help="Shows no Information. Only Logfiles", action="store_true")
			args = parser.parse_args()
			
		except:
			logging.error("cannot parse args")
		else:			
			try:
			
				#display/log args
				logging.debug(" - Frequency: %s", args.freq)
				logging.debug(" - Device: %s", args.device)
				logging.debug(" - PPM Error: %s", args.error)
				logging.debug(" - Squelch: %s", args.squelch)
				
				demodulation = ""
				if "FMS" in args.demod:
					demodulation += "-a FMSFSK "
					logging.debug(" - Demod: FMS")
				if "ZVEI" in args.demod:
					demodulation += "-a ZVEI2 "
					logging.debug(" - Demod: ZVEI")
				if "POC512" in args.demod:
					demodulation += "-a POCSAG512 "
					logging.debug(" - Demod: POC512")
				if "POC1200" in args.demod:
					demodulation += "-a POCSAG1200 "
					logging.debug(" - Demod: P")		
				if "POC2400" in args.demod:
					demodulation += "-a POCSAG2400 "
					logging.debug(" - Demod: POC2400")
				
				logging.debug(" - Verbose Mode: %s", args.verbose)
				logging.debug(" - Quiet Mode: %s", args.quiet)

				if args.verbose:
					ch.setLevel(logging.DEBUG)	
				if args.quiet:
					ch.setLevel(logging.CRITICAL)
				
				if not args.quiet: #only if not quiet mode
					print "     ____  ____  ______       __      __       __    " 
					print "    / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_  b" 
					print "   / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \ e" 
					print "  / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / / t" 
					print " /_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/  a" 
					print "            German BOS Information Script            " 
					print "                 by Bastian Schroll                  " 
					print "" 
				
					print "Frequency:   "+args.freq
					print "Device-ID:   "+str(args.device)
					print "Error in PPM:    "+str(args.error)
					print "Active Demods:   "+str(len(args.demod))
					if "FMS" in args.demod:
						print "- FMS"
					if "ZVEI" in args.demod:
						print "- ZVEI" 
					if "POC512" in args.demod:
						print "- POC512"
					if "POC1200" in args.demod:
						print "- POC1200"
					if "POC2400" in args.demod:
						print "- POC2400" 
					print "Squelch: "+str(args.squelch)
					if args.verbose:
						print "Verbose Mode!" 
					print "" 
					
			except:
				logging.exception("cannot display/log args")		
			try:	
			
				#preload vars
				logging.debug("pre-load variables")
				fms_id = 0
				fms_id_old = 0
				fms_time_old = 0
						
				zvei_id = 0
				zvei_id_old = 0
				zvei_time_old = 0
				
				poc_id = 0
				poc_id_old = 0
				poc_time_old = 0
				
			except:
				logging.debug("cannot pre-load variables")			
			try:
			
				#read config
				logging.debug("reading config file")
				globals.config = ConfigParser.ConfigParser()
				globals.config.read(globals.script_path+"/config/config.ini")
				for key,val in globals.config.items("BOSWatch"):
					logging.debug(" - %s = %s", key, val)
					
			except:
				logging.debug("cannot read config file")
			else:				
				try:
				
					#load plugins
					logging.debug("loading plugins")
					pluginList = {}
					for i in pluginloader.getPlugins():
						plugin = pluginloader.loadPlugin(i)
						pluginList[i["name"]] = plugin
						
				except:
					logging.exception("cannot load Plugins")			
				try:
				
					#start rtl_fm
					logging.debug("starting rtl_fm")
					rtl_fm = subprocess.Popen("rtl_fm -d "+str(args.device)+" -f "+str(args.freq)+" -M fm -s 22050 -p "+str(args.error)+" -E DC -F 0 -l "+str(args.squelch)+" -g 100",
							#stdin=rtl_fm.stdout,
							stdout=subprocess.PIPE,
							stderr=open(globals.script_path+"/log/rtl_fm.log","a"),
							shell=True)
							
				except:
					logging.exception("cannot start rtl_fm")
				else:				
					try:
					
						#start multimon
						logging.debug("starting multimon-ng")
						multimon_ng = subprocess.Popen("multimon-ng "+str(demodulation)+" -f alpha -t raw /dev/stdin - ",
							stdin=rtl_fm.stdout,
							stdout=subprocess.PIPE,
							stderr=open(globals.script_path+"/log/multimon.log","a"),
							shell=True)
							
					except:
						logging.exception("cannot start multimon-ng")
					else:				
						
						logging.debug("start decoding")  
						while True: 
							#RAW Data from Multimon-NG
							#ZVEI2: 25832
							#FMS: 43f314170000 (9=Rotkreuz      3=Bayern 1        Ort 0x25=037FZG 7141Status 3=Einsatz Ab    0=FZG->LST2=III(mit NA,ohneSIGNAL)) CRC correct\n' 
							decoded = str(multimon_ng.stdout.readline()) #Get line data from multimon stdout
							
							#only for develop
							#decoded = "ZVEI2: 25832"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=III(mit NA,ohneSIGNAL)) CRC correct\n'"
							#decoded = 	"POCSAG1200: Address: 1234567  Function: 1  Alpha:   XXMSG MEfeweffsjh"
							#time.sleep(1)	
							
							
							if True: #if input data avalable
								
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
											if fms_id == fms_id_old and timestamp < fms_time_old + globals.config.getint("BOSWatch", "fms_double_ignore_time"): #check for double alarm
												logging.warning("FMS double alarm: %s within %s second(s)", fms_id_old, timestamp-fms_time_old)
												fms_time_old = timestamp #in case of double alarm, fms_double_ignore_time set new
											else:
												logging.info("FMS:%s Status:%s Richtung:%s TKI:%s", fms_id[0:8], fms_status, fms_direction, fms_tsi)
												data = {"fms":fms_id[0:8], "status":fms_status, "direction":fms_direction, "tsi":fms_tsi}
												throwAlarm("FMS",data)
												
												fms_id_old = fms_id #save last id
												fms_time_old = timestamp #save last time	
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
										if zvei_id == zvei_id_old and timestamp < zvei_time_old + globals.config.getint("BOSWatch", "zvei_double_ignore_time"): #check for double alarm
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
													if poc_id == poc_id_old and timestamp < poc_time_old + globals.config.getint("BOSWatch", "poc_double_ignore_time"): #check for double alarm
														logging.warning("POCSAG%s double alarm: %s within %s second(s)", bitrate, poc_id_old, timestamp-poc_time_old)
														poc_time_old = timestamp #in case of double alarm, poc_double_ignore_time set new
													else:
														logging.info("POCSAG%s: %s %s %s ", bitrate, poc_id, poc_sub, poc_text)
														data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate}
														throwAlarm("POC",data)
										
														poc_id_old = poc_id #save last id
														poc_time_old = timestamp #save last time		
												else:
													logging.warning("POCSAG%s: %s out of filter range (high)", bitrate, poc_id)
											else:
												logging.warning("POCSAG%s: %s out of filter range (low)",bitrate, poc_id)
										else:
											logging.warning("No valid POCSAG: %s", poc_id)
								
except KeyboardInterrupt:
	logging.warning("Keyboard Interrupt")	
except:
	logging.exception("unknown error")
finally:
	try:
		logging.debug("BOSWatch shuting down")
		rtl_fm.terminate()
		logging.debug("rtl_fm terminated") 
		multimon_ng.terminate()
		logging.debug("multimon-ng terminated")
		logging.debug("exiting BOSWatch")		
	except:
		logging.warning("failed in clean-up routine")	
	finally:
		logging.info("BOSWatch exit()")	
		exit(0)