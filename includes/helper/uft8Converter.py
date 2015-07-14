#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
little Helper for converting strings

@author: Jens Herrmann
"""

import logging


def convertToUTF8(string = ""):
	"""
	Returns given string in UTF-8

	@type    string: String
	@param   string: String to convert to UTF-8

	@return:    string in UTF-8
	@exception: Exception if converting to UTF-8 failed
	"""

	uft8String = ""
	
	# nothing to do if string is empty
	if len(string) > 0:
		try:
			# check given string is already UTF-8, return
			return string.decode('UTF-8', 'strict')
		except UnicodeDecodeError:
			# string contains non-UTF-8 character
			logging.debug("string contains non-UTF-8 characters: %s", string)
			
			# try to find out encoding:
			encodings = ('windows-1250', 'windows-1252', 'latin_1', 'cp850', 'cp852', 'iso8859_2', 'iso8859_15', 'mac_latin2', 'mac_roman')
			for enc in encodings:
				try:
					string = string.decode(enc)
					logging.debug("string was encoded in: %s", enc)
					break
				except Exception:
					# if exception for last encoding entry fail, raise exception
					if enc == encodings[-1]:
						logging.warning("no encoding found")
						logging.debug("no encoding found", exc_info=True)
						# no fixing possible, raise exception
						raise
					pass
			
			# string should now decoded...
			
			try:
				# encode decoded string to UTF-8
				uft8String = string.encode('UTF-8')
			except:
				logging.warning("encoding to UTF-8 failed")
				logging.debug("encoding to UTF-8 failed", exc_info=True)
				# no fixing possible, raise exception
				raise
				
			# Now we must have an utf8-string, check it:
			try:
				uft8String.decode('UTF-8', 'strict')
				logging.debug("string converting succeeded: %s", uft8String)
			except:
				logging.warning("converting to UTF-8 failed")
				logging.debug("converting to UTF-8 failed", exc_info=True)
				# no fixing possible, raise exception
				raise
			
			# End of exception: check given string is already UTF-8
			pass
	
	return uft8String