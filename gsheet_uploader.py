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

# Handles insterting data into google spreadsheets. Creds filename comes from the
# CFG config class.
class gsheet_uploader:
    def __init__(
        self,
        gsheet: str,
        data: str,
    ):
        self._gsheet = gsheet
        self._data = data

    def upload(self) -> bool:
        
        try:
            line = self._data
            # line = "TG, (OK), 3.0 PT, F(LOLUR)X F(LOLUR)IM  (F)IC , 1-wire, groove time 22.0 seconds, (CASE I)"
            # x = csv.reader(line)
            # y = line.split(",")

            result = [x.strip() for x in line.split(",")]

            now = datetime.now()  # current date and time
            result.append(now.strftime("%d/%m/%Y"))
            result.append(now.strftime("%H:%M:%S"))
            # 	print(list(result))

            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                CFG.GOOGLE.CREDS_FILE, scope
            )
            client = gspread.authorize(creds)
            
            sheet = client.open(self._gsheet).sheet1
            row = result
            index = 2
            sheet.insert_row(row, index)

            log.info("Inserting LSO grade into Google sheet.")

            return True
        except Exception as e:
            log.debug(f'Error - {e}')
            return False



if __name__ == "__main__":
    if len(sys.argv) == 3:
        target_sheet = gsheet_uploader(sys.argv[1], sys.argv[2])
        target_sheet.upload()
    else:
        log.error("Need to supply Google sheet name and data to add to it.")
