#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
MySQL-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages to a MySQL database

@author: Jens Herrmann
@author: Bastian Schroll

@requires: MySQL-Configuration has to be set in the config.ini
@requires: Created Database/Tables, see boswatch.sql
"""

import logging # Global logger

import mysql
import mysql.connector

from includes import globalVars  # Global variables

from includes.helper import configHandler

def isSignal(poc_id):
	"""
	@type    poc_id: string
	@param   poc_id: POCSAG Ric

	@requires:  Configuration has to be set in the config.ini

	@return:    True if the Ric is Signal, other False
	@exception: none
	"""
	# If RIC is Signal return True, else False
	if globalVars.config.get("POC", "netIdent_ric"):
		if poc_id in globalVars.config.get("POC", "netIdent_ric"):
			logging.info("RIC %s is net ident", poc_id)
			return True
		else:
			logging.info("RIC %s is no net ident", poc_id)
			return False


##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine is called one time for initialize the plugin

	@requires:  nothing

	@return:    nothing
	"""
	# nothing to do for this plugin
	return


##
#
# Main function of MySQL-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the MySQL-Plugin.
	It will store the data to an MySQL database

	The configuration for the MySQL-Connection is set in the config.ini.
	For DB- and tablestructure see boswatch.sql

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending to BosMon
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch to BosMon.
	@type    freq: string
	@keyword freq: frequency is not used in this plugin

	@requires: MySQL-Configuration has to be set in the config.ini
	@requires: Created Database/Tables, see boswatch.sql

	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("MySQL"): #read and debug the config

			try:
				#
				# Connect to MySQL
				#
				logging.debug("connect to MySQL")
				connection = mysql.connector.connect(host = globalVars.config.get("MySQL","dbserver"), port = globalVars.config.get("MySQL","dbport"), user = globalVars.config.get("MySQL","dbuser"), passwd = globalVars.config.get("MySQL","dbpassword"), db = globalVars.config.get("MySQL","database"), charset='utf8mb4')
				cursor = connection.cursor()
			except:
				logging.error("cannot connect to MySQL")
				logging.debug("cannot connect to MySQL", exc_info=True)
			else: # Without connection, plugin couldn't work
				try:
					#
					# Create and execute SQL-statement
					#
					logging.debug("Insert %s", typ)

					if typ == "FMS":
						cursor.execute("INSERT INTO "+globalVars.config.get("MySQL","tableFMS")+" (`time`, `fms`, `status`, `direction`, `directionText`, `tsi`, `description`) VALUES (FROM_UNIXTIME(%s),%s,%s,%s,%s,%s,%s)", (data["timestamp"], data["fms"], data["status"], data["direction"], data["directionText"], data["tsi"], data["description"]))

					elif typ == "ZVEI":
						cursor.execute("INSERT INTO "+globalVars.config.get("MySQL","tableZVEI")+" (`time`, `zvei`, `description`) VALUES (FROM_UNIXTIME(%s),%s,%s)", (data["timestamp"], data["zvei"], data["description"]))

					elif typ == "POC":
						if isSignal(data["ric"]):
							if globalVars.config.getint("POC","netIdent_history"):
								cursor.execute("INSERT INTO "+globalVars.config.get("MySQL","tableSIG")+" (`time`,`ric`) VALUES (NOW(), '"+data["ric"]+"');")
							else:
								cursor.execute("UPDATE "+globalVars.config.get("MySQL","tableSIG")+" SET time = NOW() WHERE ric = '"+data["ric"]+"';")
								if cursor.rowcount == 0:
									cursor.execute("INSERT INTO "+globalVars.config.get("MySQL","tableSIG")+" (`time`,`ric`) VALUES (NOW(), '"+data["ric"]+"');")
						else:
							cursor.execute("INSERT INTO "+globalVars.config.get("MySQL","tablePOC")+" (`time`, `ric`, `function`, `functionChar`, `msg`, `bitrate`, `description`) VALUES (FROM_UNIXTIME(%s),%s,%s,%s,%s,%s,%s)", (data["timestamp"], data["ric"], data["function"], data["functionChar"], data["msg"], data["bitrate"], data["description"]))

					else:
						logging.warning("Invalid Typ: %s", typ)
				except:
					logging.error("cannot Insert %s", typ)
					logging.debug("cannot Insert %s", typ, exc_info=True)
					return

			finally:
				logging.debug("close MySQL")
				try:
					cursor.close()
					connection.close() #Close connection in every case
				except:
					pass

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
