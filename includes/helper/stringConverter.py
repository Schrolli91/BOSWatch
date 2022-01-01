#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
little Helper for converting strings

@author: Jens Herrmann
"""

import logging

#
# local helper function to decode a string...
#
def decodeString(inputString = ""):
	"""
	Returns given string as unicode

	@type    string: String
	@param   string: String to convert to unicode

	@return:    string in unicode
	@exception: Exception if converting to unicode failed
	"""
	decodedString = ""
	logging.debug("call decodeString('%s')", inputString)
	# try to find out encoding:
	encodings = ('utf-8', 'windows-1250', 'windows-1252', 'latin_1', 'cp850', 'cp852', 'iso8859_2', 'iso8859_15', 'mac_latin2', 'mac_roman')
	for enc in encodings:
		try:
			decodedString = inputString.decode(enc)
			logging.debug("-- string was encoded in: %s", enc)
			break
		except Exception:
			# if exception for last encoding entry fail, raise exception
			if enc == encodings[-1]:
				logging.warning("no encoding found")
				logging.debug("no encoding found", exc_info=True)
				# no fixing possible, raise exception
				raise
	return decodedString


def convertToUnicode(inputString = ""):
	"""
	Returns given string as unicode

	@type    string: String
	@param   string: String to convert to unicode

	@return:    string in unicode
	@exception: Exception if converting to unicode failed
	"""

	decodedString = ""
	logging.debug("call convertToUnicode('%s')", inputString)

	# nothing to do if inputString is empty
	if len(inputString) > 0:
		# 1. check if integer
		try:
			if int(inputString):
				logging.debug("-- integer")
				# ... then return it
				return inputString
		except ValueError:
			# ... no integer is okay...
			pass

		# 2. Check if inputString is unicode...
		if isinstance(inputString, str):
			logging.debug("-- unicode")
			return inputString

		try:
			# try to decoding:
			decodedString = decodeString(inputString)
		except:
			logging.warning("decoding string failed")
			logging.debug("encoding string failed", exc_info=True)
			# no fixing possible, raise exception
			raise
	return decodedString



def convertToUTF8(inputString = ""):
	"""
	Returns given string in UTF-8

	@type    string: String
	@param   string: String to convert to UTF-8

	@return:    string in UTF-8
	@exception: Exception if converting to UTF-8 failed
	"""

	uft8String = ""
	logging.debug("call convertToUTF8('%s')", inputString)

	# nothing to do if inputString is empty
	if len(inputString) > 0:
		try:
			# 1. check if integer
			try:
				if int(inputString):
					logging.debug("-- integer")
					# ... then return it
					return inputString
			except ValueError:
				pass

			# 2. Check if inputString is unicode...
			if isinstance(inputString, str):
				logging.debug("-- unicode")
				# ... then return it as UTF-8
				uft8String = decodedString.encode('UTF-8')
				return uft8String

			# 2. check given inputString is already UTF-8...
			decodedString = inputString.decode('UTF-8', 'strict')
			# ... no UnicodeDecodeError exception, inputString ist UTF-8
			logging.debug("-- UTF-8")
			return inputString

		except UnicodeDecodeError:
			# inputString contains non-UTF-8 character
			logging.debug("string contains non-UTF-8 characters: %s", inputString)

			try:
				# try to decoding:
				decodedString = decodeString(inputString)
			except:
				logging.warning("decoding string failed")
				logging.debug("encoding string failed", exc_info=True)
				# no fixing possible, raise exception
				raise

			# inputString should now decoded...

			try:
				# encode decodedString to UTF-8
				uft8String = decodedString.encode('UTF-8')
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

			# End of exception UnicodeDecodeError: check given string is already UTF-8

		except:
			logging.warning("error checking given string")
			logging.debug("error checking given string", exc_info=True)
			# no fixing possible, raise exception
			raise

	return uft8String
