import gspread
import json
import os
import time
import matplotlib.pyplot as plt

# import matplotlib.colors as mcolors
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties

# import numpy as np
import statistics
from oauth2client.service_account import ServiceAccountCredentials
from config.logger import logger
import config.settings as CFG

log = logger(__name__, CFG.GREENIEBOARD.FILE_BOARDROOM_LOG, "w", CFG.APP.DEBUG)


def updateDatabase(path):
    if time.time() - getModificationTimeSeconds(path) > 3600:
        log.debug("Updating from Google.")
        updateFromGoogle()
    else:
        log.info("Less than one hour since last refresh, skipping pull from google.")


def updateFromGoogle():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CFG.GOOGLE.CREDS_FILE, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(CFG.GOOGLE.SHEET_LSO_GRADES).sheet1
        list_of_hashes = sheet.get_all_records()

        with open(CFG.GREENIEBOARD.FILE_DATA_LSO, "w") as outfile:
            json.dump(list_of_hashes, outfile)
    except Exception as e:
        log.debug(f"Exception thrown in updateFromGoogle. Error - {e}")
        return

    log.info("Local HypeMan LSO grade database updated from Google Sheets.")


def getModificationTimeSeconds(path):
    ct = time.time()
    try:
        modification_time = os.path.getmtime(path)
        log.debug("Last modification time since the epoch:", modification_time)
    except OSError:
        log.debug(f"Path {path} does not exists or is inaccessible")
        return ct - 4000

    return modification_time


def printRow(row, place):
    # pp = pprint.PrettyPrinter()
    # pp.pprint(row)
    log.debug(f"{place}: {row[1]} {row[3]}/{row[4]}/{row[5]}")
    return


def isPilotQual(name):
    return False


def calculateGradeQual(curList, grade0):

    try:
        pt = float(curList[0]["points"])
        # print('(QUAL) points ', pt, ' for ', curList[0]['pilot'])
        return pt
    except Exception as e:
        log.debug(f"- {e}")
        return float(-1.0)


def calculateGradeCivilian(curList, grade0):
    grade = grade0
    pt = float(-1.0)
    x = 0
    for i in curList:
        try:
            pt = float(i["points"])
        except Exception as e:
            log.debug(f'- {e}')
            x = 0

        if pt >= 0.0:
            # print('(UNQUAL) highest score for ', i['pilot'], ' as ', pt)
            # grade['points']=pt
            return pt
        else:
            # print('No finalscore for ', i['pilot'])
            return 0.0


def calculateGrade(curList, grade0):
    if isPilotQual(curList[0]["pilot"]):
        return calculateGradeQual(curList, grade0)
    else:
        return calculateGradeCivilian(curList, grade0)


def calculatePilotRow(data, name, grade0):

    boardRow = []

    uniqueDates = []
    for i in reversed(data):
        grade = grade0
        if name == i["pilot"]:
            if i["ServerDate"] not in uniqueDates:
                uniqueDates.append(i["ServerDate"])

    for i in uniqueDates:
        # print(i)
        curList = []
        for j in data:
            if name == j["pilot"] and j["ServerDate"] == i:
                curList.append(j)

        boardRow.append(calculateGrade(curList, grade0))

    #            if not haveDate:
    #                curDate = i['ServerDate']
    #                haveDate = True
    #
    #            if curDate == i['ServerDate']:
    #                curList.append(i)
    #
    #            else:
    #                curDate = i['ServerDate']
    #                grade = calculateGrade(curList, grade0)
    #                boardRow.append(grade)
    #                curList = [];
    #                curList.append(i)

    # print(boardRow)
    return boardRow


lsoData = CFG.GREENIEBOARD.FILE_DATA_LSO
updateDatabase(lsoData)

with open(CFG.GREENIEBOARD.FILE_DATA_LSO) as json_file:
    data = json.load(json_file)

grade0 = {}
grade0["color"] = "white"
grade0["score"] = 0.0
grade0["symbol"] = "x"
grade0["grade"] = "--"

pilots = []

pilotRows = []
pilotDict = {}
# get the rows
for i in reversed(data):
    name = i["pilot"]
    if name not in pilots:
        pilots.append(name)
        # print('Calculating for: ', name)
        pilotRow = calculatePilotRow(data, name, grade0)
        print(name, " score: ", pilotRow)
        pilotRows.append(pilotRow)
        pilotDict[name] = pilotRow


# maxLength = 0
# for i in pilotRows:
#     if len(i) > maxLength:
#         maxLength = len(i)


fig = plt.figure(dpi=150)
ax = fig.add_subplot(1, 1, 1)
frame1 = plt.gca()
frame1.axes.get_xaxis().set_ticks([])
frame1.axes.get_yaxis().set_ticks([])

tb = Table(ax, bbox=[0, 0, 1, 1])

tb.auto_set_font_size(False)

# n_cols = maxLength+2
# n_rows = len(pilots)+1
width, height = 100 / CFG.GREENIEBOARD.BOARD_COL, 100.0 / CFG.GREENIEBOARD.BOARD_ROW
anchor = "⚓"
# unicorn='✈️'
blankcell = "#1A392A"
colors = ["red", "orange", "orange", "yellow", "lightgreen"]


minDate = data[-1]["ServerDate"]
maxDate = data[0]["ServerDate"]
textcolor = "#FFFFF0"
edgecolor = "#708090"
cell = tb.add_cell(
    0, 0, 3 * width, height, text="Callsign", loc="center", facecolor=blankcell
)  # edgecolor='none'
cell.get_text().set_color(textcolor)
cell.set_text_props(fontproperties=FontProperties(weight="bold", size=8))
cell.set_edgecolor(edgecolor)
# cell.set_fontsize(24)
cell = tb.add_cell(
    0, 1, width, height, text="", loc="center", facecolor=blankcell
)  # edgecolor='none'
cell.get_text().set_color(textcolor)
cell.set_edgecolor(edgecolor)
cell.set_text_props(fontproperties=FontProperties(weight="bold", size=8))
cell.set_edgecolor(edgecolor)
# cell.set_fontsize(24)
titlestr = CFG.GREENIEBOARD.BOARD_TITLE
count = 0
# for col_idx in range(2,maxLength+2):
for col_idx in range(2, CFG.GREENIEBOARD.BOARD_COL):

    text = ""

    if count < len(titlestr):
        text = titlestr[count]
        count = count + 1
    cell = tb.add_cell(
        0, col_idx, width, height, text=text, loc="center", facecolor=blankcell
    )
    cell.set_edgecolor(edgecolor)
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight="bold", size=8))
    cell.set_edgecolor(edgecolor)

# cell.set_text_props(family='')


titlestr = "JOW Greenie Board " + minDate + " to " + maxDate
for p_idx in range(0, len(pilots)):
    row_idx = p_idx + 1
    cell = tb.add_cell(
        row_idx,
        0,
        3 * width,
        height,
        text=pilots[p_idx],
        loc="center",
        facecolor=blankcell,
        edgecolor="blue",
    )  # edgecolor='none'
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight="bold", size="6"))
    cell.set_edgecolor(edgecolor)
    name = pilots[p_idx]
    rd = pilotDict[name]
    avg = statistics.mean(rd)
    cell = tb.add_cell(
        row_idx, 1, width, height, text=round(avg, 1), loc="center", facecolor=blankcell
    )
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight="bold", size="7.4"))
    cell.set_edgecolor(edgecolor)
    col_idx = 2
    for g in rd:

        text = ""
        if g == 0:
            color = colors[0]
        elif g > 0 and g < 1:
            color = colors[1]
        elif g >= 1 and g < 2:
            color = colors[2]
        elif g >= 2 and g < 3:
            text = "O"
            color = colors[3]
        elif g >= 3:
            color = colors[4]
        else:
            color = blankcell

        if g > 4.5:
            text = anchor

        cell = tb.add_cell(
            row_idx, col_idx, width, height, text=text, loc="center", facecolor=color
        )  # edgecolor='none'
        cell.get_text().set_color("#333412")
        # cell.auto_set_font_size()
        cell.set_text_props(fontproperties=FontProperties(weight="bold", size="14"))
        cell.set_edgecolor(edgecolor)
        col_idx = col_idx + 1

    color = blankcell
    text = ""

    # add the remaining cells to the end
    for f in range(col_idx, CFG.GREENIEBOARD.BOARD_COL):
        cell = tb.add_cell(
            row_idx, f, width, height, text=text, loc="center", facecolor=color
        )  # edgecolor='none'
        cell.set_edgecolor(edgecolor)


# pad the grid with blank rows
# number_of_rows = tb.
needed_rows = CFG.GREENIEBOARD.BOARD_ROW - len(pilots)
for idx in range(len(pilots) + 1, needed_rows + 2):
    cell = tb.add_cell(
        idx, 0, 3 * width, height, text=" ", loc="center", facecolor=blankcell
    )
    cell.get_text().set_color(textcolor)
    cell.set_text_props(fontproperties=FontProperties(weight="bold", size="7.5"))
    cell.set_edgecolor(edgecolor)
    for cnt in range(1, CFG.GREENIEBOARD.BOARD_COL):
        cell = tb.add_cell(
            idx, cnt, width, height, text="", loc="center", facecolor=blankcell
        )
        cell.get_text().set_color(textcolor)
        cell.set_text_props(fontproperties=FontProperties(weight="bold", size="7.5"))
        cell.set_edgecolor(edgecolor)


# tb.set_fontsize(7)
ax.add_table(tb)
ax.set_axis_off()
ax.axis("off")
plt.box(False)
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
# plt.title(titlestr,color='w')

plt.savefig(
    CFG.GREENIEBOARD.IMAGE_BOARD, transparent=False, bbox_inches="tight", pad_inches=0
)
