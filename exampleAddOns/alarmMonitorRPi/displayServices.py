#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

"""
alarmMonitor - displayServices

@author: Jens Herrmann
"""

#
# Only works as an asynchronous thread
# will call "exit(0)" when function is finished
#
def autoTurnOffDisplay():
	"""
	Asynchronous function to turn of the display backlight 
	
	@requires: globals.showDisplay        - status of backlight
	@requires: globals.enableDisplayUntil - given timestamp to turn off backlight
	@requires: globals.running            - service runs as long as this is True

	In case of an exception the function set globals.abort to True.
	This will terminate the main program.
	
	@return:    nothing
	@exception: SystemExit exception in case of an error
	"""
	
	import sys
	import time
	import logging
	import ConfigParser
	import globals

	logging.debug("autoTurnOffDisplay-thread started")
	
	try:
		# Running will be set to False if main program is shutting down
		while globals.running == True:
			# check if timestamp is in the past
			if (globals.showDisplay == True) and (globals.enableDisplayUntil < int(time.time())):
				globals.showDisplay = False
				logging.info("display turned off")
			# we will do this only one time per second
			time.sleep(1)
	except:
		logging.error("unknown error in autoTurnOffDisplay-thread")
		logging.debug("unknown error in autoTurnOffDisplay-thread", exc_info=True)
		# abort main program
		globals.abort = True
		sys.exit(1)
	finally:
		logging.debug("exit autoTurnOffDisplay-thread")
		exit(0)


#
# Only works as an asynchronous thread
# will call "exit(0)" when function is finished
#		
def eventHandler():
	"""
	Asynchronous function to handle pygames events
	in particular the touchscreen events
	
	@requires: globals.showDisplay        - status of backlight
	@requires: globals.enableDisplayUntil - timestamp to turn off backlight
	@requires: globals.running            - service runs as long as this is True
	@requires: configuration has to be set in the config.ini

	In case of an exception the function set globals.abort to True.
	This will terminate the main program.
	
	@return:    nothing
	@exception: SystemExit exception in case of an error
	"""
	import sys
	import time
	import logging
	import ConfigParser
	import pygame
	import globals

	logging.debug("eventHandler-thread called")
	
	try:
		clock = pygame.time.Clock()

		# Running will be set to False if main program is shutting down
		while globals.running == True:
			# This limits the while loop to a max of 2 times per second.
			# Leave this out and we will use all CPU we can.
			clock.tick(2)
			
			# current time for this loop:
			curtime = int(time.time())

			for event in pygame.event.get():
				# event-handler for QUIT
				if event.type == pygame.QUIT: 
					globals.running = False

				# if touchscreen pressed
				if event.type == pygame.MOUSEBUTTONDOWN:
					if globals.showDisplay:
						logging.info("turn OFF display")
						globals.showDisplay = False
					else:
						logging.info("turn ON display")
						globals.enableDisplayUntil = curtime + globals.config.getint("AlarmMonitor","showDisplayTime")
						globals.showDisplay = True
	except:
		logging.error("unknown error in eventHandler-thread")
		logging.debug("unknown error in eventHandler-thread", exc_info=True)
		# abort main program
		globals.abort = True
		sys.exit(1)
	finally:
		logging.debug("exit eventHandler-thread")
		exit(0)
		
		
#
# Only works as an asynchronous thread
# will call "exit(0)" when function is finished
#
def displayPainter():
	"""
	Asynchronous function to build the display content
	
	@requires: globals.showDisplay        - status of backlight
	@requires: globals.enableDisplayUntil - given timestamp when backlight will turned off
	@requires: globals.running            - service runs as long as this is True
	@requires: globals.data               - data of the last alarm
	@requires: globals.lastAlarm          - timestamp of the last processing (see alarmRICs and keepAliveRICs) 
	@requires: configuration has to be set in the config.ini

	In case of an exception the function set globals.abort to True.
	This will terminate the main program.
	
	@return:    nothing
	@exception: SystemExit exception in case of an error
	"""
	
	import sys
	import time
	import logging
	import ConfigParser
	import RPi.GPIO as GPIO
	import pygame
	from wrapline import wrapline
	import globals

	logging.debug("displayPainter-thread called")
	
	try:
		# use GPIO pin numbering convention
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		# set up GPIO pin for output
		GPIO.setup(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.OUT)

		pygame.init()

		#screen size
		size = (globals.config.getint("Display","displayWidth"), globals.config.getint("Display","displayHeight"))
		screen = pygame.display.set_mode(size)

		# disable mouse cursor
		pygame.mouse.set_visible(False)
		
		#define fonts
		fontHeader = pygame.font.Font(None, 30)
		fontHeader.set_bold(True)
		fontHeader.set_underline(True)

		fontRIC = pygame.font.Font(None, 30)
		fontRIC.set_bold(True)

		fontMsg = pygame.font.Font(None, 20)
		fontTime = pygame.font.Font(None, 15)
		
		clock = pygame.time.Clock()

		logging.debug("displayPainter-thread started")
		
		# Running will be set to False if main program is shutting down
		while globals.running == True:
			# This limits the while loop to a max of 2 times per second.
			# Leave this out and we will use all CPU we can.
			clock.tick(2)
			
			# current time for this loop:
			curtime = int(time.time())
					
			if globals.showDisplay:
				# Enable LCD display
				GPIO.output(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.HIGH)
				# Clear the screen and set the screen background
				screen.fill(globals.screenBackground)
				
				widthX = globals.config.getint("Display","displayWidth") - 20
				widthY = globals.config.getint("Display","displayHeight") - 20
				pygame.draw.rect(screen, pygame.Color(globals.config.get("AlarmMonitor","colourBlack")), (10, 10, widthX, widthY))

				# header
				header = fontHeader.render("Alarm-Monitor", 1, pygame.Color(globals.config.get("AlarmMonitor","colourRed")))
				(width, height) = fontHeader.size("Alarm-Monitor")
				x = (int(globals.config.getint("Display","displayWidth")) - width)/2
				screen.blit(header, (x, 20))
				
				# Alarm - RIC:
				try:
					y = 50
					textLines = wrapline(globals.data['description'], fontRIC, (globals.config.getint("Display","displayWidth") - 40))
					for index, item in enumerate(textLines):
						textZeile = fontRIC.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
						screen.blit(textZeile, (20, y))
						y += 25
				except KeyError:
					pass
				
				# Alarm - Text
				try:
					y += 10
					textLines = wrapline(globals.data['msg'].replace("*", " * "), fontMsg, (globals.config.getint("Display","displayWidth") - 40))
					for index, item in enumerate(textLines):
						textZeile = fontMsg.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
						screen.blit(textZeile, (20, y))
						y += 20
				except KeyError:
					pass
				
				# show time of last alarm
				if globals.lastAlarm > 0:
					try:
						# format last alarm
						lastAlarmString = time.strftime("%H:%M:%S", time.localtime(globals.lastAlarm))
						# Color time:
						# red: lastAlarm more than n (delayForRed) seconds past
						if (int(globals.lastAlarm) + globals.config.getint("AlarmMonitor","delayForRed")) < curtime:
							timeColour = pygame.Color(globals.config.get("AlarmMonitor","colourRed"))
						# yellow: lastAlarm more than n (delayForYellow) seconds past
						elif (int(globals.lastAlarm) + globals.config.getint("AlarmMonitor","delayForYellow")) < curtime:
							timeColour = pygame.Color(globals.config.get("AlarmMonitor","colourYellow"))
						# dgrey: normal
						else:
							timeColour = pygame.Color(globals.config.get("AlarmMonitor","colourGreen"))
						lastAlarm = fontTime.render(lastAlarmString, 1, timeColour)
						(width, height) = fontTime.size(lastAlarmString)
						x = globals.config.getint("Display","displayWidth") - 20 - width
						screen.blit(lastAlarm, (x, 20))
					except:
						logging.debug("unknown error in lastAlarm", exc_info=True)
						pass
				
				# show remaining time before display will be turned off:
				restZeit = globals.enableDisplayUntil - curtime +1
				zeit = fontTime.render(str(restZeit), 1, pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")))
				screen.blit(zeit, (20, 20))
			else:
				GPIO.output(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.LOW)
			
			# Update display...
			pygame.display.update()

	except:
		logging.error("unknown error in displayPainter-thread")
		logging.debug("unknown error in displayPainter-thread", exc_info=True)
		# abort main program
		globals.abort = True
		sys.exit(1)
	finally:
		logging.debug("exit displayPainter-thread")
		GPIO.output(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.LOW)
		GPIO.cleanup()
		pygame.quit()
		exit(0)