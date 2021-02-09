import csv
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config.logger import logger
import config.settings as CFG

import random
from time import sleep

log = logger(__name__, CFG.GOOGLE.FILE_GOOGLE_LOG, "w", CFG.APP.DEBUG)

# add a random delay to every upload entry.  The goal here is to prevent too many requests from happening at once
# and to prevent the case of two requests happening at exactly the same time, such as during a formation landing
# luvit/lua seem to be able to handle the rapid fire of UDP data coming from DCS, but the google sheets API
# limits the number of queries it will accept
sleep(random.uniform(1.0, 30))

if len(sys.argv) == 2:
	
	line = sys.argv[1]	

	result = [x.strip() for x in line.split(',')]
	
	# now = datetime.now() # current date and time
	# result.append(now.strftime("%d/%m/%Y"))
	# result.append(now.strftime("%H:%M:%S"))
	# print(list(result))
	
	scope = [
				'https://spreadsheets.google.com/feeds',
				'https://www.googleapis.com/auth/drive'
			]
	creds = ServiceAccountCredentials.from_json_keyfile_name(
        CFG.GOOGLE.CREDS_FILE, scope)
	client = gspread.authorize(creds)

	sheet = client.open(CFG.GOOGLE.SHEET_FLIGHT_STATS).sheet1

	log.info("Adding entry into Flight Stats Google sheet.")

	row = result
	index = 2
	sheet.insert_row(row, index)