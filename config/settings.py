import os

class APP:
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 10081
    FOLDER_IMG = os.path.join(os.getcwd(), 'images')
    FOLDER_DATA = os.path.join(os.getcwd(), 'data')
    FOLDER_LOGS = os.path.join(os.getcwd(), 'logs')
    FILE_LOG = os.path.join(FOLDER_LOGS, 'hypeman.log')

class GOOGLE:
    CREDS_FILE = 'lso-grade-sheet-265019-66cf26ebfe79.json'
    SHEET_LSO_GRADES = 'LSO_Grades'
    SHEET_FLIGHT_STATS = 'Flight_Stats'

class GREENIEBOARD:
    DATA_LSO = os.path.join(APP.FOLDER_DATA, 'lso_data.txt')
    BOARD_TITLE = 'JOINT OPS WING '
    BOARD_COL = 17
    BOARD_ROW = 15

class TRAPSHEET:
    # folder where DCS outputs the trapsheets
    LOCATION = 'C:/Users/nascar/Saved Games/DCS.openbeta_server'

class SERVERINFO:
    # servers to check
    SERVERS = [
        ['JOW West', 'jow.aggressors.ca'],
        ['JOW East', 'jow2.aggressors.ca'],
        ['localhost', '127.0.0.1']
    ]
    # ports on each server to check
    PORTS = [
        ['DCS', 10308],
        ['SRS', 5002],
        ['LOTAC', 10310]
    ]
    # log file name and location
    FILE_LOG = os.path.join(APP.FOLDER_LOGS, 'server_info.log')

    # data output file name and location
    FILE_DATA = os.path.join(APP.FOLDER_DATA, 'server_info.txt')
