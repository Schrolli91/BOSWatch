#!/usr/bin/python
# -*- coding: cp1252 -*-
#

"""
TERM-Handler for use script as a daemon
In order for the Python program to exit gracefully when the TERM signal is received,
it must have a function that exits the program when signal.SIGTERM is received.

@author: 		Jens Herrmann
"""

import logging
import signal       # for use as daemon
import sys          # throw SystemExitException when daemon is terminated

def sigterm_handler(_signo, _stack_frame):
	"""
	TERM-Handler for use script as a daemon

	@type    _signo: signalnum
	@param   _signo: signal number
	@type    _stack_frame: frame object
	@param   _stack_frame: current stack frame

	@exception: SystemExitException when daemon is terminated
	"""
	logging.warning("TERM signal received")
	sys.exit(0)

# Set the handler for signal to the function handler.
signal.signal(signal.SIGTERM, sigterm_handler)
