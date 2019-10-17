#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Function to expand the dataset with a description.

@author: Jens Herrmann

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import csv # for loading the description files
import re # for matching IDs with a regular expression

from includes import globalVars  # Global variables
from includes.helper import stringConverter


# local variables
fmsDescribtionList  = {}
zveiDescribtionList = {}
ricDescribtionList  = {}


##
#
# Local function will load the csv-file
#
def loadCSV(typ, idField):
	"""
	Local function for loading csv-file into python list
	Structure: [id] = description

	@return:    Python list of descriptions
	"""
	resultList = {}
	try:
		logging.debug("-- loading %s.csv", typ)
		with open(globalVars.script_path+'/csv/'+typ+'.csv') as csvfile:
			# DictReader expected structure described in first line of csv-file
			reader = csv.DictReader(csvfile)
			for row in reader:
				logging.debug(row)
				# only import rows with an integer as id, allow subrics though
				if re.match("^[0-9A-F]+$", row[idField], re.IGNORECASE):
					try:
						resultList[row[idField].lower()] = stringConverter.convertToUTF8(row['description'])
					except:
						# skip entry in case of an exception
						pass
		logging.debug("-- loading csv finished")
	except:
		logging.error("loading csvList for typ: %s failed", typ)
		logging.debug("loading csvList for typ: %s failed", typ, exc_info=True)
		raise
	return resultList;


##
#
# call this for loading the description lists
#
def loadDescriptionLists():
	"""
	Load data from the csv-files in global description list for FMS, ZVEI and POCSAG

	@return:    nothing
	@exception: Exception if loading failed
	"""
	try:
		logging.debug("loading description lists")

		if globalVars.config.getint("FMS", "idDescribed"):
			logging.debug("- load FMS description list")
			global fmsDescribtionList
			fmsDescribtionList = loadCSV("fms", "fms")

		if globalVars.config.getint("ZVEI", "idDescribed"):
			logging.debug("- load ZVEI description list")
			global zveiDescribtionList
			zveiDescribtionList = loadCSV("zvei", "zvei")

		if globalVars.config.getint("POC", "idDescribed"):
			logging.debug("- load pocsag description list")
			global ricDescribtionList
			ricDescribtionList = loadCSV("poc", "ric")

	except:
		logging.error("cannot load description lists")
		logging.debug("cannot load description lists", exc_info=True)


##
#
# public function for getting a description
#
def getDescription(typ, data):
	"""
	Get description for id.
	Will return id if no description will be found.

	@return:    description as string
	"""
	resultStr = data
	logging.debug("look up description lists")
	try:
		if typ == "FMS":
			resultStr = fmsDescribtionList[data]
		elif typ == "ZVEI":
			resultStr = zveiDescribtionList[data]
		elif typ == "POC":
			resultStr = ricDescribtionList[data[:-1]] # MainRIC
			resultStr += " " + ricDescribtionList[data] # SubRIC
		else:
			logging.warning("Invalid Typ: %s", typ)

	except KeyError:
		# will be thrown when there is no description for the id
		# -> nothing to do...
		pass

	except:
		logging.error("Error during look up description lists")
		logging.debug("Error during look up description lists", exc_info=True)

	logging.debug(" - result for %s: %s", data, resultStr)
	return resultStr
