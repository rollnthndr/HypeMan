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
    FILE_GOOGLE_LOG = os.path.join(APP.FOLDER_LOGS, 'google_sheet.log')
    CREDS_FILE = 'lso-grade-sheet-265019-66cf26ebfe79.json'
    SHEET_LSO_GRADES = 'LSO_Grades'
    SHEET_FLIGHT_STATS = 'Flight_Stats'


class GREENIEBOARD:
    FILE_BOARDROOM_LOG = os.path.join(APP.FOLDER_LOGS, 'boardroom.log')
    FILE_BOARDROOM_COMPOSE_LOG = os.path.join(APP.FOLDER_LOGS, 'boardroom_compose.log')
    FILE_DATA_LSO = os.path.join(APP.FOLDER_DATA, 'lso_data.txt')
    BOARD_TITLE = '416 Lynx Squadron '
    BOARD_COL = 17
    BOARD_ROW = 15
    IMAGE_BOARD = os.path.join(APP.FOLDER_IMG, 'board.png')
    IMAGE_BOARDROOM = os.path.join(APP.FOLDER_IMG, 'boardroom.jpg')
    IMAGE_BOARDROOM_MASK = os.path.join(APP.FOLDER_IMG, 'boardroom_mask.png')
    IMAGE_BOARDROOM_FINAL = os.path.join(APP.FOLDER_IMG, 'boardroom_final.jpg')


class TRAPSHEET:
    # folder where DCS outputs the trapsheets
    FOLDER_LOCATION = 'C:/Users/nascar/Saved Games/DCS.openbeta_server'
    FILE_TRAPESHEET_LOG = os.path.join(APP.FOLDER_LOGS, 'trapsheet.log')
    IMAGE_BOAT_TOP = os.path.join(APP.FOLDER_IMG, 'boat_top.png')
    IMAGE_BOAT_SIDE = os.path.join(APP.FOLDER_IMG, 'boat_side.png')
    IMAGE_TRAPESHEET = os.path.join(APP.FOLDER_IMG, 'trapesheet.png')


class SERVERINFO:
    # servers to check
    SERVERS = [
        # ['JOW West', 'jow.aggressors.ca'],
        # ['JOW East', 'jow2.aggressors.ca'],
        ['Great Ballz Of Fire', '127.0.0.1']
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
    FILE_DATA = os.path.join(APP.FOLDER_DATA, 'server_info_data.txt')
