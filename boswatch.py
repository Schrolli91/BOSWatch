#!/usr/bin/python
# -*- coding: cp1252 -*-

##### Info #####
# BOSWatch
# Python Script to Recive and Decode German BOS Information with rtl_fm and multimon-NG
# For more Information see the README.md
##### Info #####

import time
#import sys
import subprocess
#import os
import mysql
import mysql.connector

import argparse #for parse the args
import ConfigParser #for parse the config file
import re #Regex


def curtime(format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format)	

def stop_script(err):
	print ""
	print "ERR: "+err
	try:
		if useMySQL: #only if MySQL is active
			if args.verbose: print "disconnect MySQL" 
			connection.close()
		rtl_fm.terminate()
		if args.verbose: print "rtl_fm terminated" 
		multimon_ng.terminate()
		if args.verbose: print "multimon-ng terminated" 
		if args.verbose: print "exiting BOSWatch"
	except:
		pass


#With -h or --help you get the Args help
#ArgsParser
parser = argparse.ArgumentParser(prog="boswatch.py", description="BOSWatch is a Python Script to Recive and Decode German BOS Information with rtl_fm and multimon-NG", epilog="More Options you can find in the extern config.ini File in this Folder")
#parser.add_argument("-c", "--channel", help="BOS Channel you want to listen")
parser.add_argument("-f", "--freq", help="Frequency you want to listen", required=True)
parser.add_argument("-d", "--device", help="Device you want to use (Check with rtl_test)", type=int, default=0)
parser.add_argument("-e", "--error", help="Frequency-Error of your Device in PPM", type=int, default=0)
parser.add_argument("-a", "--demod", help="Demodulation Functions", choices=['FMS', 'ZVEI', 'POC512', 'POC1200', 'POC2400'], required=True, nargs="+")
parser.add_argument("-s", "--squelch", help="Level of Squelch", type=int, default=0)
parser.add_argument("-v", "--verbose", help="Shows more Information", action="store_true")
args = parser.parse_args()


#Read Data from Args, Put it into working Variables and Display them
print("#########################")
print("#                       #")
print("#     BOSWatch beta     #")
print("#                       #")
print("#########################")
print("")

freq = args.freq
print "Frequency:	"+freq
	
#channel = args.channel
#print("Frequency:	",channel)

device = args.device
print "Device-ID:	"+str(device)

error = args.error
print "Error in PPM:	"+str(error)

demodulation = ""
print "Active Demods:	"+str(len(args.demod))
if "FMS" in args.demod:
	demodulation += "-a FMSFSK "
	print "- FMS"
if "ZVEI" in args.demod:
	demodulation += "-a ZVEI2 "
	print "- ZVEI" 
if "POC512" in args.demod:
	demodulation += "-a POCSAG512 "
	print "- POC512"
if "POC1200" in args.demod:
	demodulation += "-a POCSAG1200 "
	print "- POC1200"
if "POC2400" in args.demod:
	demodulation += "-a POCSAG2400 "
	print "- POC2400" 

squelch = args.squelch
print "Squelch:	"+str(squelch)

if args.verbose:
	print("Verbose Mode!")

print ""	
	
try:	
	#ConfigParser
	if args.verbose: print "reading config file"
	try:
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		fms_double_ignore_time = int(config.get("FMS", "double_ignore_time"))
		zvei_double_ignore_time = int(config.get("ZVEI", "double_ignore_time"))
		
		#MySQL config
		useMySQL = int(config.get("MySQL", "useMySQL")) #use MySQL support?
		if useMySQL: #only if MySQL is active
			dbserver = config.get("MySQL", "dbserver")
			dbuser = config.get("MySQL", "dbuser")
			dbpassword = config.get("MySQL", "dbpassword")
			database = config.get("MySQL", "database")
		
			#MySQL tables
			tableFMS = config.get("MySQL", "tableFMS")
			tableZVEI = config.get("MySQL", "tableZVEI")
			tablePOC = config.get("MySQL", "tablePOC") 
	except:
		stop_script("config reading error")
		exit(0)
	
	
	if useMySQL: #only if MySQL is active
		if args.verbose: print "connect to MySQL database"
		try:
			connection = mysql.connector.connect(host = str(dbserver), user = str(dbuser), passwd = str(dbpassword), db = str(database))
		except:
			print "MySQL connect error"
			exit(0)
	
	#variables pre-load
	if args.verbose: print "pre-load variables"
	fms_id = 0
	fms_id_old = 0
	fms_time_old = 0
	
	zvei_id = 0
	zvei_id_old = 0
	zvei_time_old = 0

	
	if args.verbose: print "starting rtl_fm"
	try:
		rtl_fm = subprocess.Popen("rtl_fm -d "+str(device)+" -f "+str(freq)+" -M fm -s 22050 -p "+str(error)+" -E DC -F 0 -l "+str(squelch)+" -g 100",
									#stdin=rtl_fm.stdout,
									stdout=subprocess.PIPE,
									stderr=open('log.txt','a'),
									shell=True)
	except:
		stop_script("cannot start rtl_fm")
		exit(0)
		
	#multimon_ng = subprocess.Popen("aplay -r 22050 -f S16_LE -t raw",
	if args.verbose: print "starting multimon-ng"
	try:
		multimon_ng = subprocess.Popen("multimon-ng "+str(demodulation)+" -f alpha -t raw /dev/stdin - ",
									stdin=rtl_fm.stdout,
									stdout=subprocess.PIPE,
									stderr=open('log.txt','a'),
									shell=True)
	except:
		stop_script("cannot start multimon-ng")
		exit(0)
				
				   
	if args.verbose: print "start decoding"	
	print ""
	while True:	
		#RAW Data from Multimon-NG
		#ZVEI2: 25832
		#FMS: 43f314170000 (9=Rotkreuz      3=Bayern 1        Ort 0x25=037FZG 7141Status 3=Einsatz Ab    0=FZG->LST2=III(mit NA,ohneSIGNAL)) CRC correct\n'	
		decoded = str(multimon_ng.stdout.readline()) #Get line data from multimon stdout
		
		if True: #if input data avalable
		
			timestamp = int(time.time())#Get Timestamp					
			#if args.verbose: print "RAW: "+decoded #for verbose mode, print Raw input data
				
			#FMS Decoder Section	
			#check FMS: -> check CRC -> validate -> check double alarm -> print -> (MySQL)
			if "FMS:" in decoded:	
				if args.verbose: print "recived FMS"
					
				fms_service = decoded[19]		#Organisation
				fms_country = decoded[36] 		#Bundesland
				fms_location = decoded[65:67]	#Ort
				fms_vehicle = decoded[72:76]	#Fahrzeug
				fms_status = decoded[84]		#Status
				fms_direction = decoded[101]	#Richtung
				fms_tsi = decoded[114:117]		#Taktische Kruzinformation
				
				if "CRC correct" in decoded: #check CRC is correct	
					fms_id = fms_service+fms_country+fms_location+fms_vehicle+fms_status+fms_direction #build FMS id
					if re.search("[0-9]{8}[0-9a-f]{1}[01]{1}", fms_id): #if FMS is valid
						if fms_id == fms_id_old and timestamp < fms_time_old + fms_double_ignore_time: #check for double alarm
							if args.verbose: print "FMS double alarm: "+fms_id_old
							fms_time_old = timestamp #in case of double alarm, fms_double_ignore_time set new
						else:
							print curtime("%H:%M:%S")+" BOS:"+fms_service+" Bundesland:"+fms_country+" Ort:"+fms_location+" Fahrzeug:"+fms_vehicle+" Status:"+fms_status+" Richtung:"+fms_direction+" TKI:"+fms_tsi
							fms_id_old = fms_id #save last id
							fms_time_old = timestamp #save last time	
							
							if useMySQL: #only if MySQL is active
								cursor = connection.cursor()
								cursor.execute("INSERT INTO "+tableFMS+" (time,service,country,location,vehicle,status,direction,tsi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(curtime(),fms_service,fms_country,fms_location,fms_vehicle,fms_status,fms_direction,fms_tsi))
								cursor.close()
								connection.commit()
					elif args.verbose: #Invalid error only in verbose mode
						print "No valid FMS: "+fms_id		
				elif args.verbose: #crc error only in verbose mode
					print "CRC incorrect"
				
				
			#ZVEI Decoder Section
			#check ZVEI: -> validate -> check double alarm -> print -> (MySQL)	 
			if "ZVEI2:" in decoded:
				if args.verbose: print "recived ZVEI" 
					
				zvei_id = decoded[7:12]	#ZVEI Code	
				if re.search("[0-9F]{5}", zvei_id): #if ZVEI is valid
					if zvei_id == zvei_id_old and timestamp < zvei_time_old + zvei_double_ignore_time: #check for double alarm
						if args.verbose: print "ZVEI double alarm: "+zvei_id_old
						zvei_time_old = timestamp #in case of double alarm, zvei_double_ignore_time set new
					else:
						print curtime("%H:%M:%S")+" 5-Ton: "+zvei_id
						zvei_id_old = zvei_id #save last id
						zvei_time_old = timestamp #save last time
						
						if useMySQL: #only if MySQL is active
							cursor = connection.cursor()
							cursor.execute("INSERT INTO "+tableZVEI+" (time,zvei) VALUES (%s,%s)",(curtime(),zvei_id))
							cursor.close()
							connection.commit()
						
				elif args.verbose: #Invalid error only in verbose mode
					print "No valid ZVEI: "+zvei_id
	
		
except KeyboardInterrupt:
	stop_script("Keyboard Interrupt")