#!/usr/bin/python
# -*- coding: cp1252 -*-
#
# BOSWatch
# Autor: Bastian Schroll
# 
#

"""
Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG
For more Information see the README.md
"""

import logging
import logging.handlers

import argparse #for parse the args
import ConfigParser #for parse the config file
import os #for log mkdir
import time #timestamp
import subprocess

from includes import globals  # Global variables

##
# This Class extended the TimedRotatingFileHandler with the possibility to change the backupCount after initialization.
##
class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
	"""Extended Version of TimedRotatingFileHandler"""
	def setBackupCount(self, backupCount):
		"""Set/Change backupCount"""
		self.backupCount = backupCount

#
# Programm
#
try:
	try:	
		#
		# Script-pathes
		#
		globals.script_path = os.path.dirname(os.path.abspath(__file__))
		
		#
		# If necessary create Log-Path
		#
		if not os.path.exists(globals.script_path+"/log/"):
			os.mkdir(globals.script_path+"/log/")

		#
		# Create new myLogger...
		#
		myLogger = logging.getLogger()
		myLogger.setLevel(logging.DEBUG)
		#set log string format
		formatter = logging.Formatter('%(asctime)s - %(module)-12s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
		#create a file logger
		fh = MyTimedRotatingFileHandler(globals.script_path+"/log/boswatch.log", "midnight", interval=1, backupCount=999)
		#Starts with log level >= Debug
		#will be changed with config.ini-param later
		fh.setLevel(logging.DEBUG) 
		fh.setFormatter(formatter)
		myLogger.addHandler(fh)
		#create a display logger
		ch = logging.StreamHandler()
		#log level for display >= info
		#will be changed later after parsing args
		ch.setLevel(logging.INFO) 
		ch.setFormatter(formatter)
		myLogger.addHandler(ch)		
	except:
		logging.exception("cannot create logger")
	else:	
		
		try:
			#
			# Clear the logfiles
			#
			fh.doRollover()
			rtl_log = open(globals.script_path+"/log/rtl_fm.log", "w")
			mon_log = open(globals.script_path+"/log/multimon.log", "w")
			rtl_log.write("")
			mon_log.write("")
			rtl_log.close()
			mon_log.close()
			logging.debug("BOSWatch has started")
			logging.debug("Logfiles cleared")		
		except:
			logging.exception("cannot clear Logfiles")	
			
		try:
			#
			# Parse args
			#
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
				#
				# For debug display/log args
				#
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
				#
				# Read config.ini
				#
				logging.debug("reading config file")
				globals.config = ConfigParser.ConfigParser()
				globals.config.read(globals.script_path+"/config/config.ini")
				for key,val in globals.config.items("BOSWatch"):
					logging.debug(" - %s = %s", key, val)
			except:
				logging.exception("cannot read config file")
			else:
				
				try:
					# 
					# Set the loglevel and backupCount of the file handler 
					#
					logging.debug("set loglevel of fileHandler to: %s",globals.config.getint("BOSWatch","loglevel") )
					fh.setLevel(globals.config.getint("BOSWatch","loglevel"))
					logging.debug("set backupCount of fileHandler to: %s", globals.config.getint("BOSWatch","backupCount"))
					fh.setBackupCount(globals.config.getint("BOSWatch","backupCount"))
				except:
					logging.exception("cannot set loglevel of fileHandler")
				
				#
				# Load plugins
				#
				from includes import pluginLoader
				pluginLoader.loadPlugins()
				
				#
				# Load filters
				#
				if globals.config.getint("BOSWatch","useRegExFilter"):
					from includes import filter
					filter.loadFilters()
				
				try:				
					#
					# Start rtl_fm
					#
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
						#
						# Start multimon
						#
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
							#
							# Get decoded data from multimon-ng and call BOSWatch-decoder
							#
						
							# RAW Data from Multimon-NG
							# ZVEI2: 25832
							# FMS: 43f314170000 (9=Rotkreuz      3=Bayern 1        Ort 0x25=037FZG 7141Status 3=Einsatz Ab    0=FZG->LST2=III(mit NA,ohneSIGNAL)) CRC correct\n' 
							# POCSAG1200: Address: 1234567  Function: 1  Alpha:   Hello World
							decoded = str(multimon_ng.stdout.readline()) #Get line data from multimon stdout
							
							# Test-strings only for develop
							#decoded = "ZVEI2: 25832"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=I  (ohneNA,ohneSIGNAL)) CRC correct\n'"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=I  (ohneNA,ohneSIGNAL)) CRC correct\n'"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=II (ohneNA,mit SIGNAL)) CRC correct\n'"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     1=LST->FZG 2=III(mit NA,ohneSIGNAL)) CRC correct\n'"
							#decoded = "FMS: 43f314170000 (9=Rotkreuz       3=Bayern 1         Ort 0x25=037FZG  7141Status  3=Einsatz Ab     0=FZG->LST 2=IV (mit NA,mit SIGNAL)) CRC correct\n'"
							#decoded = "POCSAG1200: Address: 1234567  Function: 1  Alpha:   Hello World"
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
		# Close Logging
		logging.debug("close Logging")	
		logging.shutdown()
		fh.close()
		ch.close()
		logging.info("BOSWatch exit()")
		exit(0)
