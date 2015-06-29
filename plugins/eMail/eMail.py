#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
eMail-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages via eMail/SMTP

@author: Jens Herrmann

@requires: eMail-Configuration has to be set in the config.ini
"""

import logging # Global logger

import time
import smtplib #for the SMTP client
from email.mime.text import MIMEText # Import the email modules we'll need
from email.utils import formatdate # need for confirm to RFC2822 standard
from email.utils import make_msgid # need for confirm to RFC2822 standard

from includes import globals  # Global variables

##
#
# onLoad function of plugin
# will be called by the pluginLoader
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine are called

	@requires:  nothing
	
	@return:    nothing
	"""
	try:
		########## User onLoad CODE ##########
		
		########## User onLoad CODE ##########
		
	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)

##
#
# Private helper function for a printable Timestamp
#
def curtime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

##
#
# do send mail
#
def doSendmail(server, subject, mailtext):
	"""
	This local function send the eMail

	@type  server:   SMTP
	@param server:   An SMTP-Object that represents an open connection to an eMail-Server
	@type  subject:  string
	@param subject:  Subject for the eMail
	@type  mailtext: string
	@param mailtext: Mailtext for the eMail
	
	@return:    nothing
	@exception: Exception if smtp.sendmail failed
	"""
	try: 
		msg = MIMEText(mailtext)
		msg['From'] = globals.config.get("eMail", "from")
		msg['To']   = globals.config.get("eMail", "to")
		msg['Subject'] = subject
		msg['Date'] = formatdate()
		msg['Message-Id'] = make_msgid()
		msg['Priority'] = globals.config.get("eMail", "priority")
		server.sendmail(globals.config.get("eMail", "from"), globals.config.get("eMail", "to"), msg.as_string())
	except:
		logging.error("send eMail failed")
		logging.debug("send eMail failed", exc_info=True)
		raise


##
#
# Main function of eMail-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the eMail-Plugin.
	It will send the data via eMail (SMTP)
	
	The configuration for the eMail-Connection is set in the config.ini.
	If an user is set, the HTTP-Request is authenticatet.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending via eMail
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to eMail.
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  eMail-Configuration has to be set in the config.ini
	
	@return:    nothing
	"""
	try:
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("eMail"):
				logging.debug(" - %s = %s", key, val)
				
		except:
			logging.error("cannot read config file")
			logging.debug("cannot read config file", exc_info=True)
		else: # Without config, plugin couldn't work

			try:
					#
				# connect to SMTP-Server
				#
				server = smtplib.SMTP(globals.config.get("eMail", "smtp_server"), globals.config.get("eMail", "smtp_port"))
				# debug-level to shell (0=no debug|1)
				server.set_debuglevel(0)
				
				# if tls is enabled, starttls
				if globals.config.get("eMail", "tls"):
					server.starttls()
				
				# if user is given, login
				if globals.config.get("eMail", "user"):
					server.login(globals.config.get("eMail", "user"), globals.config.get("eMail", "password"))
				
			except:
				logging.error("cannot connect to eMail")
				logging.debug("cannot connect to eMail", exc_info=True)
				# Without connection, plugin couldn't work
				return

			else:

				if typ == "FMS":
					logging.debug("Start FMS to eMail")
					try:
						# read subject-structure from config.ini
						subject = globals.config.get("eMail", "fms_subject")
						subject = subject.replace("%FMS%", data["fms"]).replace("%STATUS%", data["status"]) #replace Wildcards
						subject = subject.replace("%DIR%", data["direction"]).replace("%DIRT%", data["directionText"]) #replace Wildcards
						subject = subject.replace("%TSI%", data["tsi"]) #replace Wildcards
						subject = subject.replace("%DESCR%", data["description"]) # replace Wildcards
						subject = subject.replace("%TIME%", curtime()) # replace Wildcards
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "fms_message")
						mailtext = mailtext.replace("%FMS%", data["fms"]).replace("%STATUS%", data["status"]) #replace Wildcards
						mailtext = mailtext.replace("%DIR%", data["direction"]).replace("%DIRT%", data["directionText"]) #replace Wildcards
						mailtext = mailtext.replace("%TSI%", data["tsi"]) #replace Wildcards
						mailtext = mailtext.replace("%DESCR%", data["description"]) # replace Wildcards
						mailtext = mailtext.replace("%TIME%", curtime()) # replace Wildcards
						# send eMail
						doSendmail(server, subject, mailtext)
					except:
						logging.error("%s to eMail failed", typ)
						logging.debug("%s to eMail failed", typ, exc_info=True)
						return

				elif typ == "ZVEI":
					logging.debug("Start ZVEI to eMail")
					try:
						# read subject-structure from config.ini
						subject = globals.config.get("eMail", "zvei_subject")
						subject = subject.replace("%ZVEI%", data["zvei"]) #replace Wildcards
						subject = subject.replace("%DESCR%", data["description"]) # replace Wildcards
						subject = subject.replace("%TIME%", curtime()) # replace Wildcards
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "zvei_message")
						mailtext = mailtext.replace("%ZVEI%", data["zvei"]) #replace Wildcards
						mailtext = mailtext.replace("%DESCR%", data["description"]) # replace Wildcards
						mailtext = mailtext.replace("%TIME%", curtime()) # replace Wildcards
						# send eMail
						doSendmail(server, subject, mailtext)
					except:
						logging.error("%s to eMail failed", typ)
						logging.debug("%s to eMail failed", typ, exc_info=True)
						return

				elif typ == "POC":
					logging.debug("Start POC to eMail")
					try:
						# read subject-structure from config.ini
						subject = globals.config.get("eMail", "poc_subject")
						subject = subject.replace("%RIC%", data["ric"]) #replace Wildcards
						subject = subject.replace("%FUNC%", data["function"]).replace("%FUNCCHAR%", data["functionChar"]) #replace Wildcards
						subject = subject.replace("%MSG%", data["msg"]).replace("%BITRATE%", str(data["bitrate"])) #replace Wildcards
						subject = subject.replace("%DESCR%", data["description"]) # replace Wildcards
						subject = subject.replace("%TIME%", curtime()) # replace Wildcards
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "poc_message")
						mailtext = mailtext.replace("%RIC%", data["ric"]) #replace Wildcards
						mailtext = mailtext.replace("%FUNC%", data["function"]).replace("%FUNCCHAR%", data["functionChar"]) #replace Wildcards
						mailtext = mailtext.replace("%MSG%", data["msg"]).replace("%BITRATE%", str(data["bitrate"])) #replace Wildcards
						mailtext = mailtext.replace("%DESCR%", data["description"]) # replace Wildcards
						mailtext = mailtext.replace("%TIME%", curtime()) # replace Wildcards
						# send eMail
						doSendmail(server, subject, mailtext)
					except:
						logging.error("%s to eMail failed", typ)
						logging.debug("%s to eMail failed", typ, exc_info=True)
						return
				
				else:
					logging.warning("Invalid Typ: %s", typ)	

			finally:
				logging.debug("close eMail-Connection")
				try: 
					server.quit()
				except:
					pass
			
	except:
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)