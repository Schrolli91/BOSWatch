#!/usr/bin/python
# -*- coding: cp1252 -*-

##### Info #####
# BOSWatch
# Autor: Bastian Schroll
# Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG
# For more Information see the README.md
##### Info #####

import logging

import argparse #for parse the args
import ConfigParser #for parse the config file
import os #for log mkdir
import time #timestamp
import subprocess

from includes import globals  # Global variables

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
					from includes import shellHeader
					shellHeader.printHeader(args)					
			except:
				logging.exception("cannot display/log args")		

			try:		
				#read config
				logging.debug("reading config file")
				globals.config = ConfigParser.ConfigParser()
				globals.config.read(globals.script_path+"/config/config.ini")
				for key,val in globals.config.items("BOSWatch"):
					logging.debug(" - %s = %s", key, val)
			except:
				logging.exception("cannot read config file")
			else:
				
				try:
					#set the loglevel of the file handler
					logging.debug("set loglevel of fileHandler")
					fh.setLevel(globals.config.getint("BOSWatch","loglevel"))
				except:
					logging.exception("cannot set loglevel of fileHandler")
				
				#load plugins
				from includes import pluginLoader
				pluginLoader.loadPlugins()
				
				#load filters
				from includes import filter
				filter.getFilters()
				
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
							#decoded = 	"POCSAG1200: Address: 1234567  Function: 1  Alpha:   Hello World"
							#time.sleep(1)	
							
							from includes import decoder
							decoder.decode(args.freq, decoded)
								
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
