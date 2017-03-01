#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
"""
BOSWatch
Python script to receive and decode German BOS information with rtl_fm and multimon-NG
Through a simple plugin system, data can easily be transferred to other applications
For more information see the README.md

@author: 		Bastian Schroll
@author: 		Jens Herrmann

Thanks to smith_fms and McBo from Funkmeldesystem.de - Forum for Inspiration and Groundwork!

GitHUB:		https://github.com/Schrolli91/BOSWatch
"""

import logging
import logging.handlers

import argparse     # for parse the args
import ConfigParser # for parse the config file
import os           # for log mkdir
import time         # for time.sleep()
import subprocess   # for starting rtl_fm and multimon-ng

from includes import globalVars  # Global variables
from includes import MyTimedRotatingFileHandler  # extension of TimedRotatingFileHandler
from includes import checkSubprocesses  # check startup of the subprocesses
from includes.helper import configHandler
from includes.helper import freqConverter

#
# Check for exisiting config/config.ini-file
#
if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/config/config.ini"):
	print "ERROR: No config.ini found"
	exit(1)

#
# ArgParser
# Have to be before main program
#
try:
	# With -h or --help you get the Args help
	parser = argparse.ArgumentParser(prog="boswatch.py",
									description="BOSWatch is a Python Script to recive and decode german BOS information with rtl_fm and multimon-NG",
									epilog="More options you can find in the extern config.ini file in the folder /config")
	# parser.add_argument("-c", "--channel", help="BOS Channel you want to listen")
	parser.add_argument("-f", "--freq", help="Frequency you want to listen to", required=True)
	parser.add_argument("-d", "--device", help="Device you want to use (check with rtl_test)", type=int, default=0)
	parser.add_argument("-e", "--error", help="Frequency-error of your device in PPM", default=0)
	parser.add_argument("-a", "--demod", help="Demodulation functions", choices=['FMS', 'ZVEI', 'POC512', 'POC1200', 'POC2400'], required=True, nargs="+")
	parser.add_argument("-s", "--squelch", help="Level of squelch", type=int, default=0)
	parser.add_argument("-g", "--gain", help="Level of gain", type=int, default=100)
	parser.add_argument("-u", "--usevarlog", help="Use '/var/log/boswatch' for logfiles instead of subdir 'log' in BOSWatch directory", action="store_true")
	parser.add_argument("-v", "--verbose", help="Show more information", action="store_true")
	parser.add_argument("-q", "--quiet", help="Show no information. Only logfiles", action="store_true")
	# We need this argument for testing (skip instantiate of rtl-fm and multimon-ng):
	parser.add_argument("-t", "--test", help=argparse.SUPPRESS, action="store_true")
	args = parser.parse_args()
except SystemExit:
	# -h or --help called, exit right now
	exit(0)
except:
	# we couldn't work without arguments -> exit
	print "ERROR: cannot parsing the arguments"
	exit(1)


#
# Main program
#
try:
	# initialization:
	rtl_fm = None
	multimon_ng = None
	nmaHandler = None

	try:
		#
		# Script-pathes
		#
		globalVars.script_path = os.path.dirname(os.path.abspath(__file__))

		#
		# Set log_path
		#
		if args.usevarlog:
			globalVars.log_path = "/var/log/BOSWatch/"
		else:
			globalVars.log_path = globalVars.script_path+"/log/"

		#
		# If necessary create log-path
		#
		if not os.path.exists(globalVars.log_path):
			os.mkdir(globalVars.log_path)
	except:
		# we couldn't work without logging -> exit
		print "ERROR: cannot initialize paths"
		exit(1)

	#
	# Create new myLogger...
	#
	try:
		myLogger = logging.getLogger()
		myLogger.setLevel(logging.DEBUG)
		# set log string format
		#formatter = logging.Formatter('%(asctime)s - %(module)-15s %(funcName)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
		formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
		# create a file logger
		fh = MyTimedRotatingFileHandler.MyTimedRotatingFileHandler(globalVars.log_path+"boswatch.log", "midnight", interval=1, backupCount=999)
		# Starts with log level >= Debug
		# will be changed with config.ini-param later
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(formatter)
		myLogger.addHandler(fh)
		# create a display logger
		ch = logging.StreamHandler()
		# log level for display: Default: info
		if args.verbose:
			ch.setLevel(logging.DEBUG)
		elif args.quiet:
			ch.setLevel(logging.CRITICAL)
		else:
			ch.setLevel(logging.INFO)
		ch.setFormatter(formatter)
		myLogger.addHandler(ch)

	except:
		# we couldn't work without logging -> exit
		print "ERROR: cannot create logger"
		exit(1)

	# initialization of the logging was fine, continue...
	try:
		#
		# Clear the logfiles
		#
		fh.doRollover()
		rtl_log = open(globalVars.log_path+"rtl_fm.log", "w")
		mon_log = open(globalVars.log_path+"multimon.log", "w")
		rawMmOut = open(globalVars.log_path+"mm_raw.txt", "w")
		rtl_log.write("")
		mon_log.write("")
		rawMmOut.write("")
		rtl_log.close()
		mon_log.close()
		rawMmOut.close()
		logging.debug("BOSWatch has started")
		logging.debug("Logfiles cleared")

	except:
		# It's an error, but we could work without that stuff...
		logging.error("cannot clear Logfiles")
		logging.debug("cannot clear Logfiles", exc_info=True)

	#
	# For debug display/log args
	#
	try:
		logging.debug("SW Version:	%s",globalVars.versionNr)
		logging.debug("Build Date:	%s",globalVars.buildDate)
		logging.debug("BOSWatch given arguments")
		if args.test:
			logging.debug(" - Test-Mode!")

		logging.debug(" - Frequency: %s", freqConverter.freqToHz(args.freq))
		logging.debug(" - Device: %s", args.device)
		logging.debug(" - PPM Error: %s", args.error)
		logging.debug(" - Squelch: %s", args.squelch)
		logging.debug(" - Gain: %s", args.gain)

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
			logging.debug(" - Demod: POC1200")
		if "POC2400" in args.demod:
			demodulation += "-a POCSAG2400 "
			logging.debug(" - Demod: POC2400")

		logging.debug(" - Use /var/log: %s", args.usevarlog)
		logging.debug(" - Verbose Mode: %s", args.verbose)
		logging.debug(" - Quiet Mode: %s", args.quiet)

		if not args.quiet: #only if not quiet mode
			from includes import shellHeader
			shellHeader.printHeader(args)

		if args.test:
			logging.warning("!!! We are in Test-Mode !!!")

	except:
		# we couldn't work without config -> exit
		logging.critical("cannot display/log args")
		logging.debug("cannot display/log args", exc_info=True)
		exit(1)

	#
	# Read config.ini
	#
	try:
		logging.debug("reading config file")
		globalVars.config = ConfigParser.ConfigParser()
		globalVars.config.read(globalVars.script_path+"/config/config.ini")
		# if given loglevel is debug:
		if globalVars.config.getint("BOSWatch","loglevel") == 10:
			configHandler.checkConfig("BOSWatch")
			configHandler.checkConfig("FMS")
			configHandler.checkConfig("ZVEI")
			configHandler.checkConfig("POC")
	except:
		# we couldn't work without config -> exit
		logging.critical("cannot read config file")
		logging.debug("cannot read config file", exc_info=True)
		exit(1)


	#
	# Set the loglevel and backupCount of the file handler
	#
	try:
		logging.debug("set loglevel of fileHandler to: %s",globalVars.config.getint("BOSWatch","loglevel"))
		fh.setLevel(globalVars.config.getint("BOSWatch","loglevel"))
		logging.debug("set backupCount of fileHandler to: %s", globalVars.config.getint("BOSWatch","backupCount"))
		fh.setBackupCount(globalVars.config.getint("BOSWatch","backupCount"))
	except:
		# It's an error, but we could work without that stuff...
		logging.error("cannot set loglevel of fileHandler")
		logging.debug("cannot set loglevel of fileHandler", exc_info=True)


	#
	# Add NMA logging handler
	#
	try:
		if configHandler.checkConfig("NMAHandler"):
			# is NMAHandler enabled?
			if globalVars.config.getboolean("NMAHandler", "enableHandler") == True:
				# we only could do something, if an APIKey is given:
				if len(globalVars.config.get("NMAHandler","APIKey")) > 0:
					logging.debug("add NMA logging handler")
					from includes import NMAHandler
					if globalVars.config.get("NMAHandler","appName") == "":
						nmaHandler = NMAHandler.NMAHandler(globalVars.config.get("NMAHandler","APIKey"))
					else:
						nmaHandler = NMAHandler.NMAHandler(globalVars.config.get("NMAHandler","APIKey"), globalVars.config.get("NMAHandler","appName"))
					nmaHandler.setLevel(globalVars.config.getint("NMAHandler","loglevel"))
					myLogger.addHandler(nmaHandler)
	except:
		# It's an error, but we could work without that stuff...
		logging.error("cannot add NMA logging handler")
		logging.debug("cannot add NMA logging handler", exc_info=True)


	# initialization was fine, continue with main program...

	#
	# Load plugins
	#
	try:
		from includes import pluginLoader
		pluginLoader.loadPlugins()
	except:
		# we couldn't work without plugins -> exit
		logging.critical("cannot load Plugins")
		logging.debug("cannot load Plugins", exc_info=True)
		exit(1)

	#
	# Load filters
	#
	try:
		if globalVars.config.getboolean("BOSWatch","useRegExFilter"):
			from includes import regexFilter
			regexFilter.loadFilters()
	except:
		# It's an error, but we could work without that stuff...
		logging.error("cannot load filters")
		logging.debug("cannot load filters", exc_info=True)

	#
	# Load description lists
	#
	try:
		if globalVars.config.getboolean("FMS","idDescribed") or globalVars.config.getboolean("ZVEI","idDescribed") or globalVars.config.getboolean("POC","idDescribed"):
			from includes import descriptionList
			descriptionList.loadDescriptionLists()
	except:
		# It's an error, but we could work without that stuff...
		logging.error("cannot load description lists")
		logging.debug("cannot load description lists", exc_info=True)

	#
	# Start rtl_fm
	#
	try:
		if not args.test:
			logging.debug("starting rtl_fm")
			command = ""
			if globalVars.config.has_option("BOSWatch","rtl_path"):
				command = globalVars.config.get("BOSWatch","rtl_path")
			command = command+"rtl_fm -d "+str(args.device)+" -f "+str(freqConverter.freqToHz(args.freq))+" -M fm -p "+str(args.error)+" -E DC -F 0 -l "+str(args.squelch)+" -g "+str(args.gain)+" -s 22050"
			rtl_fm = subprocess.Popen(command.split(),
					#stdin=rtl_fm.stdout,
					stdout=subprocess.PIPE,
					stderr=open(globalVars.log_path+"rtl_fm.log","a"),
					shell=False)
			# rtl_fm doesn't self-destruct, when an error occurs
			# wait a moment to give the subprocess a chance to write the logfile
			time.sleep(3)
			checkSubprocesses.checkRTL()
		else:
			logging.warning("!!! Test-Mode: rtl_fm not started !!!")
	except:
		# we couldn't work without rtl_fm -> exit
		logging.critical("cannot start rtl_fm")
		logging.debug("cannot start rtl_fm", exc_info=True)
		exit(1)

	#
	# Start multimon
	#
	try:
		if not args.test:
			logging.debug("starting multimon-ng")
			command = ""
			if globalVars.config.has_option("BOSWatch","multimon_path"):
				command = globalVars.config.get("BOSWatch","multimon_path")
			command = command+"multimon-ng "+str(demodulation)+" -f alpha -t raw /dev/stdin - "
			multimon_ng = subprocess.Popen(command.split(),
				stdin=rtl_fm.stdout,
				stdout=subprocess.PIPE,
				stderr=open(globalVars.log_path+"multimon.log","a"),
				shell=False)
			# multimon-ng  doesn't self-destruct, when an error occurs
			# wait a moment to give the subprocess a chance to write the logfile
			time.sleep(3)
			checkSubprocesses.checkMultimon()
		else:
			logging.warning("!!! Test-Mode: multimon-ng not started !!!")
	except:
		# we couldn't work without multimon-ng -> exit
		logging.critical("cannot start multimon-ng")
		logging.debug("cannot start multimon-ng", exc_info=True)
		exit(1)

	#
	# Get decoded data from multimon-ng and call BOSWatch-decoder
	#
	if not args.test:
		logging.debug("start decoding")
		while True:
			decoded = str(multimon_ng.stdout.readline()) #Get line data from multimon stdout
			from includes import decoder
			decoder.decode(freqConverter.freqToHz(args.freq), decoded)

			# write multimon-ng raw data
			if globalVars.config.getboolean("BOSWatch","writeMultimonRaw"):
				try:
					rawMmOut = open(globalVars.log_path+"mm_raw.txt", "a")
					rawMmOut.write(decoded)
				except:
					logging.warning("cannot write raw multimon data")
				finally:
					rawMmOut.close()
	else:
		logging.debug("start testing")
		testFile = open(globalVars.script_path+"/citest/testdata.txt","r")
		for testData in testFile:
			if (len(testData.rstrip(' \t\n\r')) > 1) and ("#" not in testData[0]):
				logging.info("Testdata: %s", testData.rstrip(' \t\n\r'))
				from includes import decoder
				decoder.decode(freqConverter.freqToHz(args.freq), testData)
				#time.sleep(1)
		logging.debug("test finished")

except KeyboardInterrupt:
	logging.warning("Keyboard Interrupt")
except SystemExit:
	# SystemExitException is thrown if daemon was terminated
	logging.warning("SystemExit received")
	# only exit to call finally-block
	exit()
except:
	logging.exception("unknown error")
finally:
	try:
		logging.debug("BOSWatch shuting down")
		if multimon_ng and multimon_ng.pid:
			logging.debug("terminate multimon-ng (%s)", multimon_ng.pid)
			multimon_ng.terminate()
			multimon_ng.wait()
			logging.debug("multimon-ng terminated")
		if rtl_fm and rtl_fm.pid:
			logging.debug("terminate rtl_fm (%s)", rtl_fm.pid)
			rtl_fm.terminate()
			rtl_fm.wait()
			logging.debug("rtl_fm terminated")
		logging.debug("exiting BOSWatch")
	except:
		logging.warning("failed in clean-up routine")
		logging.debug("failed in clean-up routine", exc_info=True)

	finally:
		# Close Logging
		logging.debug("close Logging")
		# Waiting for all Threads to write there logs
		if globalVars.config.getboolean("BOSWatch","processAlarmAsync") == True:
			logging.debug("waiting 3s for threads...")
			time.sleep(3)
		logging.info("BOSWatch exit()")
		logging.shutdown()
		if nmaHandler:
			nmaHandler.close()
		fh.close()
		ch.close()
