#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
little Helper to handle config data
for direct use in plugins to save code

@author: Bastian Schroll
"""

import logging
from includes import globalVars


def checkConfig(section=""):
	"""
	Reads the config option from an section and prints it to debug log

	@type    section: string
	@param   section: Section name from config.ini

	@return:    true (false if reading failed)
	@exception: Exception if Error at read an debug
	"""
	try:
		if section is not "": # read only data if section is given
			logging.debug("read [%s] from config file", section)

			for key,val in globalVars.config.items(section):
				if ("password" in key) or ("apikey" in key):
					val = "***"
				logging.debug(" - %s = %s", key, val)

		return True
	except:
		logging.warning("error in config read/debug")
		logging.debug("error in config read/debug", exc_info=True)
		return False
