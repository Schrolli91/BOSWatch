#!/usr/bin/python
# -*- coding: cp1252 -*-
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
