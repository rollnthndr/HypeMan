import csv
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

GOOGLE_LSO_FILE = 'LSO_Grades'
GOOGLE_CREDS_FILE = 'lso-grade-sheet-265019-66cf26ebfe79.json'

#print('Length of sys.argv:')
#print(len(sys.argv))
if len(sys.argv) == 2:
	
	line = sys.argv[1]	
	# line = "TG, (OK), 3.0 PT, F(LOLUR)X F(LOLUR)IM  (F)IC , 1-wire, groove time 22.0 seconds, (CASE I)"
	#x = csv.reader(line)
	#y = line.split(",")

	result = [x.strip() for x in line.split(',')]
	
	now = datetime.now() # current date and time
	result.append(now.strftime("%d/%m/%Y"))
	result.append(now.strftime("%H:%M:%S"))
#	print(list(result))
	
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
	client = gspread.authorize(creds)

	sheet = client.open(GOOGLE_LSO_FILE).sheet1
	#list_of_hashes = sheet.get_all_records()


	print('Inserting LSO grade into Google sheet...')

	row = result
#	print(row)

	index = 2
	sheet.insert_row(row, index)
	
#	print('Done!')
