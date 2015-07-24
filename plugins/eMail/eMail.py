#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

from includes.helper import timeHandler # helper function
from includes.helper import configHandler # helper function
from includes.helper import wildcardHandler # helper function

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
		msg = MIMEText(mailtext, 'plain', 'UTF-8')
		msg['From'] = globals.config.get("eMail", "from")
		msg['To']   = globals.config.get("eMail", "to")
		msg['Subject'] = subject
		msg['Date'] = formatdate()
		msg['Message-Id'] = make_msgid()
		msg['Priority'] = globals.config.get("eMail", "priority")
		server.sendmail(globals.config.get("eMail", "from"), globals.config.get("eMail", "to").split(), msg.as_string())
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
		if configHandler.checkConfig("eMail"): #read and debug the config

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
						# replace wildcards with helper function
						subject = wildcardHandler.replaceWildcards(subject, data)
						
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "fms_message")
						# replace wildcards with helper function
						mailtext = wildcardHandler.replaceWildcards(mailtext, data)
						
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
						# replace wildcards with helper function
						subject = wildcardHandler.replaceWildcards(subject, data)
						
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "zvei_message")
						# replace wildcards with helper function
						mailtext = wildcardHandler.replaceWildcards(mailtext, data)
						
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
						# replace wildcards with helper function
						subject = wildcardHandler.replaceWildcards(subject, data)
						
						# read mailtext-structure from config.ini
						mailtext = globals.config.get("eMail", "poc_message")
						# replace wildcards with helper function
						mailtext = wildcardHandler.replaceWildcards(mailtext, data)
						
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
