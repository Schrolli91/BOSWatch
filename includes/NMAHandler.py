#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Logging Handler for NotifyMyAndroid

@author: Jens Herrmann
"""

import logging
from includes.pynma import pynma

class NMAHandler(logging.Handler): # Inherit from logging.Handler
	"""
	Handler instances dispatch logging events to NotifyMyAndroid.
	"""
	
	def __init__(self, APIKey, application="BOSWatch", event="Logging-Handler"):
		"""
		Initializes the handler with NMA-specific parameters.
		
		@param   APIKey:      might be a string containing 1 key or an array of keys
		@param   application: application name [256]
		@param   event:       event name       [1000]
		"""
		# run the regular Handler __init__
		logging.Handler.__init__(self)
		# Our custom argument
		self.APIKey = APIKey
		self.application = application
		self.event = event
		self.nma = pynma.PyNMA(self.APIKey)


	def emit(self, record):
		"""
		Send logging record via NMA
		"""
		# record.message is the log message
		# record.levelno is the log level
		# loglevel: 10 = debug    => priority: -2
		# loglevel: 20 = info     => priority: -1
		# loglevel: 30 = warning  => priority:  0
		# loglevel: 40 = error    => priority:  1
		# loglevel: 50 = critical => priority:  2
		if record.levelno >= 50:
			priority = 2
		elif record.levelno >= 40:
			priority = 1
		elif record.levelno >= 30:
			priority = 0
		elif record.levelno >= 20:
			priority = -1
		else:
			priority = -2
		self.nma.push(self.application, self.event, record.message, priority=priority)