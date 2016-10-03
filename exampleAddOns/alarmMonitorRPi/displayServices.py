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
	import globalData

	logging.debug("autoTurnOffDisplay-thread started")

	try:
		# Running will be set to False if main program is shutting down
		while globals.running == True:
			# check if timestamp is in the past
			if (globals.showDisplay == True) and (globals.enableDisplayUntil < int(time.time())):
				globals.showDisplay = False
				globals.navigation = "alarmPage"
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
	import globalData

	logging.debug("eventHandler-thread started")

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
					(posX, posY) = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
					#logging.debug("position: (%s, %s)", posX, posY)

					# touching the screen will stop alarmSound in every case
					pygame.mixer.stop()

					# touching the dark display will turn it on for n sec
					if globals.showDisplay == False:
						logging.info("turn ON display")
						globals.enableDisplayUntil = curtime + globals.config.getint("AlarmMonitor","showDisplayTime")
						globals.navigation == "alarmPage"
						globals.showDisplay = True
					else:
						# touching the enabled display will be content sensitive...
						# if top 2/3: turn of display
						yBoundary = globals.config.getint("Display","displayHeight") - 80
						if 0 <= posY <= yBoundary:
							logging.info("turn OFF display")
							globals.showDisplay = False
							globals.navigation = "alarmPage"
						else:
							# we are in the navigation area
							globals.enableDisplayUntil = curtime + globals.config.getint("AlarmMonitor","showDisplayTime")
							if 0 <= posX <= 110:
								globals.navigation = "historyPage"
							elif 111 <= posX <= 210:
								globals.navigation = "statusPage"
							else:
								globals.screenBackground = pygame.Color(globals.config.get("AlarmMonitor","colourGreen"))
								globals.navigation = "alarmPage"
					## end if showDisplay
				## end if event MOUSEBUTTONDOWN
			## end for event
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
	from roundrects import round_rect
	import globalData

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

		fontTime = pygame.font.Font(None, 15)

		fontRIC = pygame.font.Font(None, 30)
		fontRIC.set_bold(True)
		fontMsg = pygame.font.Font(None, 20)
		fontHistory = pygame.font.Font(None, 15)

		fontStatus = pygame.font.Font(None, 20)
		fontStatus.set_bold(True)
		fontStatusContent = pygame.font.Font(None, 20)

		fontButton = pygame.font.Font(None, 20)

		clock = pygame.time.Clock()

		# Build Lists out of config-entries
		functionCharTestAlarm = [x.strip() for x in globals.config.get("AlarmMonitor","functionCharTestAlarm").replace(";", ",").split(",")]

		logging.debug("displayPainter-thread started")

		# Running will be set to False if main program is shutting down
		while globals.running == True:
			# This limits the while loop to a max of 2 times per second.
			# Leave this out and we will use all CPU we can.
			clock.tick(2)

			# current time for this loop:
			curtime = int(time.time())

			if globals.showDisplay == True:
				# Enable LCD display
				GPIO.output(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.HIGH)
				# Clear the screen and set the screen background
				screen.fill(globals.screenBackground)
				# paint black rect, so Background looks like a boarder
				widthX = globals.config.getint("Display","displayWidth") - 20
				widthY = globals.config.getint("Display","displayHeight") - 20
				pygame.draw.rect(screen, pygame.Color(globals.config.get("AlarmMonitor","colourBlack")), (10, 10, widthX, widthY))
				# header
				header = fontHeader.render("Alarm-Monitor", 1, pygame.Color(globals.config.get("AlarmMonitor","colourRed")))
				(width, height) = fontHeader.size("Alarm-Monitor")
				x = (int(globals.config.getint("Display","displayWidth")) - width)/2
				screen.blit(header, (x, 20))

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
				## end if globals.lastAlarm > 0

				# show remaining time before display will be turned off:
				restZeit = globals.enableDisplayUntil - curtime +1
				zeit = fontTime.render(str(restZeit), 1, pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")))
				screen.blit(zeit, (20, 20))

				#
				# content given by navigation:
				# default is "alarmPage"
				#
				# Startpoint for content
				if globals.navigation == "historyPage":
					try:
						y = 50
						for data in reversed(globals.alarmHistory):
							# Layout:
							# Date Description
							# Time Msg

							# Prepare date/time block
							dateString = time.strftime("%d.%m.%y", time.localtime(data['timestamp']))
							timeString = time.strftime("%H:%M:%S", time.localtime(data['timestamp']))
							if int(fontHistory.size(dateString)[0]) > int(fontHistory.size(timeString)[0]):
								(shifting, height) = fontHistory.size(dateString)
							else:
								(shifting, height) = fontHistory.size(timeString)
							shifting += 5

							# get colour
							if data['functionChar'] in functionCharTestAlarm:
								colour = globals.config.get("AlarmMonitor","colourYellow")
							else:
								colour = globals.config.get("AlarmMonitor","colourRed")

							# Paint Date/Time
							screen.blit(fontHistory.render(dateString, 1, pygame.Color(colour)), (20, y))
							screen.blit(fontHistory.render(timeString, 1, pygame.Color(colour)), (20, y + height))

							# Paint Description
							try:
								textLines = wrapline(data['description'], fontHistory, (globals.config.getint("Display","displayWidth") - shifting - 40))
								for index, item in enumerate(textLines):
									textZeile = fontHistory.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
									screen.blit(textZeile, (20 + shifting, y))
									y += height
							except KeyError:
								pass

							# Paint Msg
							try:
								textLines = wrapline(data['msg'].replace("*", " * "), fontHistory, (globals.config.getint("Display","displayWidth") - shifting - 40))
								for index, item in enumerate(textLines):
									textZeile = fontHistory.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
									screen.blit(textZeile, (20 + shifting, y))
									y += height
							except KeyError:
								pass

							# line spacing for next dataset
							y += 2

						## end for globals.alarmHistory

					except KeyError:
						pass
				## end if globals.navigation == "historyPage"

				elif globals.navigation == "statusPage":
					(width, height) = fontStatusContent.size("Anzahl Test-Alarme:")
					y = 70
					x = width + 10
					# Running since:
					title = fontStatusContent.render("Gestartet:", 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
					content = fontStatusContent.render(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(globals.startTime)), 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
					screen.blit(title,   (20,    y))
					screen.blit(content, (20 +x, y))
					y += height + 10

					# Last Alarm
					title = fontStatusContent.render("Letzte Nachricht:", 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
					if globals.lastAlarm > 0:
						content = fontStatusContent.render(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(globals.lastAlarm)), 1, timeColour)
					else:
						content = fontStatusContent.render("-", 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
					screen.blit(title,   (20,    y))
					screen.blit(content, (20 +x, y))
					y += height + 10

					# Number of Alarms
					title = fontStatusContent.render("Anzahl Alarme:", 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
					content = fontStatusContent.render(str(globals.countAlarm), 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
					screen.blit(title,   (20,    y))
					screen.blit(content, (20 +x, y))
					y += height + 10

					# Number of TestAlarms
					title = fontStatusContent.render("Anzahl Test-Alarme:", 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
					content = fontStatusContent.render(str(globals.countTestAlarm), 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
					screen.blit(title,   (20,    y))
					screen.blit(content, (20 +x, y))
					y += height + 10

					# Number of DAU-Msgs
					title = fontStatusContent.render("Anzahl DAU-Tests:", 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
					content = fontStatusContent.render(str(globals.countKeepAlive), 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
					screen.blit(title,   (20,    y))
					screen.blit(content, (20 +x, y))
					y += height + 10

				## end if globals.navigation == "statusPage"

				else:
					y = 50

					# Paint Date/Time
					try:
						dateTimeString = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(globals.data['timestamp']))
						dateTimeRow = fontStatus.render(dateTimeString, 1, pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")))
						(width, height) = fontStatus.size(dateTimeString)
						x = (int(globals.config.getint("Display","displayWidth")) - width)/2
						screen.blit(dateTimeRow, (x, y))
						y += height + 10
					except KeyError:
						pass

					# Paint Description
					try:
						textLines = wrapline(globals.data['description'], fontRIC, (globals.config.getint("Display","displayWidth") - 40))
						(width, height) = fontStatus.size(globals.data['description'])
						for index, item in enumerate(textLines):
							textRow = fontRIC.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourWhite")))
							screen.blit(textRow, (20, y))
							y += height + 5
					except KeyError:
						pass

					# Paint Msg
					try:
						y += 10
						textLines = wrapline(globals.data['msg'].replace("*", " * "), fontMsg, (globals.config.getint("Display","displayWidth") - 40))
						(width, height) = fontStatus.size(globals.data['msg'])
						for index, item in enumerate(textLines):
							textRow = fontMsg.render(item, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
							screen.blit(textRow, (20, y))
							y += height
					except KeyError:
						pass
				## end if default navigation

				# paint navigation buttons
				buttonWidth = 80
				buttonHeight = 25
				buttonY = globals.config.getint("Display","displayHeight") - buttonHeight - 2

				round_rect(screen, ( 20, buttonY, buttonWidth, buttonHeight), pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")), 10, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
				buttonText = fontButton.render("Verlauf", 1, pygame.Color(globals.config.get("AlarmMonitor","colourBlack")))
				(width, height) = fontButton.size("Verlauf")
				textX = 20 + (buttonWidth - width)/2
				textY = buttonY + (buttonHeight - height)/2
				screen.blit(buttonText, (textX, textY))

				round_rect(screen, (120, buttonY, buttonWidth, buttonHeight), pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")), 10, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
				buttonText = fontButton.render("Status", 1, pygame.Color(globals.config.get("AlarmMonitor","colourBlack")))
				(width, height) = fontButton.size("Status")
				textX = 120 + (buttonWidth - width)/2
				textY = buttonY + (buttonHeight - height)/2
				screen.blit(buttonText, (textX, textY))

				round_rect(screen, (220, buttonY, buttonWidth, buttonHeight), pygame.Color(globals.config.get("AlarmMonitor","colourDimGrey")), 10, 1, pygame.Color(globals.config.get("AlarmMonitor","colourGrey")))
				buttonText = fontButton.render("Gelesen", 1, pygame.Color(globals.config.get("AlarmMonitor","colourBlack")))
				(width, height) = fontButton.size("Gelesen")
				textX = 220 + (buttonWidth - width)/2
				textY = buttonY + (buttonHeight - height)/2
				screen.blit(buttonText, (textX, textY))

			## end if globals.showDisplay == True

			else:
				GPIO.output(globals.config.getint("Display","GPIOPinForBacklight"), GPIO.LOW)

			# Update display...
			pygame.display.update()
		## end while globals.running == True

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
