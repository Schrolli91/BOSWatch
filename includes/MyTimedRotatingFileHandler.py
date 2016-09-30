#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
This Class extended the TimedRotatingFileHandler with the possibility
to change the backupCount after initialization.

@author: 		Jens Herrmann
"""

import logging

class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
	"""Extended Version of TimedRotatingFileHandler"""
	def setBackupCount(self, backupCount):
		"""Set/Change backupCount"""
		self.backupCount = backupCount
		
	def close(self):
		"""Make shure logfile will be flushed"""
		self.flush()
		super(self.__class__, self).close()
