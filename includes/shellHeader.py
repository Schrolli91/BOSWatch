#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Shows the header in shell if quiet mode is not active

@author: Bastian Schroll
@author: Jens Herrmann

@requires: none
"""

from includes import globals

def printHeader(args):
	"""
	Prints the header to the shell

	@type    args: Array
	@param   args: All given arguments from argsparser

	@return:    nothing
	"""
	try:
		print "     ____  ____  ______       __      __       __   "
		print "    / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_  "
		print "   / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \ "
		print "  / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / / "
		print " /_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/  "
		print "            German BOS Information Script           "
		print "          by Bastian Schroll, Jens Herrmann         "
		print ""
		print "SW Version:	"+globals.getVers("vers")
		print "Build Date:	"+globals.getVers("date")
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
		if args.test:
			print "Test Mode!"
		print ""
	except:
		logging.error("cannot display shell header")
		logging.debug("cannot display shell header", exc_info=True)
