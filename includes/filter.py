#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger

from includes import globals  # Global variables


def getFilters():
	logging.debug("reading config file")
	try:
		for key,val in globals.config.items("Filters"):
			logging.debug(" - %s = %s", key, val)
			filter = val.split(";")
			globals.filterList.append({"name": key, "typ": filter[0], "plugin": filter[1], "regex": filter[2]})
	except:
		logging.exception("cannot read config file")
