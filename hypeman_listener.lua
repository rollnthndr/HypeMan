
local string = require('string') -- load standard string library included with lua
JSON = (loadfile "JSON.lua")() -- one-time load of JSON

dofile('private_api_keys.lua')

DATA_FOLDER = 'data'
IMG_FOLDER = 'images'

-------------------------------------------------------------------------------
-- private_api_keys.lua you must create, it looks like the following:
-- HypeMan BotID and Channel
--PRIVATE_HYPEMAN_BOT_CLIENT_ID = 'Bot NTIzOTasdfc2.Dv3hMw.zepasdfJPxKzdTOLA'
--PRIVATE_HYPEMAN_CHANNEL_ID = '525434328534'  -- #music
-- Carrier Grade BotID and Channel
--PRIVATE_CQ_CLIENT_ID = 'Bot NjAzMzk5MasdfOTI4.XTe80Q._Ccsy9qmnytCasdfhE'
--PRIVATE_CQ_CHANNEL_ID = '6034126353296670' -- #snafu
-- SERVERNAME = 'Rob Rules!!11!'
-------------------------------------------------------------------------------

-- Private Command ID, allow someone to send !commands to HypeMan through discord private message
-- currently uses !connect and !disconnect for hypeman_voice to connect to a Discord voice channel
PRIVATE_COMMAND_ID = '361935537571102720'
print(PRIVATE_HYPEMAN_BOT_CLIENT_ID)
print(PRIVATE_HYPEMAN_CHANNEL_ID)

local BOT_CLIENT_ID = PRIVATE_HYPEMAN_BOT_CLIENT_ID
local CHANNEL_ID = PRIVATE_HYPEMAN_CHANNEL_ID

local CQ_BOT_ID = PRIVATE_CQ_CLIENT_ID
local CQ_BOT_CHANNEL_ID = PRIVATE_CQ_CHANNEL_ID

local privmsgid = PRIVATE_COMMAND_ID

local announce_hypeman_start = false
local PORT =  10081
local HOST = '127.0.0.1'

local dgram = require('dgram')
local discordia = require('discordia')

local client = discordia.Client()
local ch = nil

local cqbot = discordia.Client()
local cqch = nil

function tableHasKey(table,key)
    return table[key] ~= nil
end

client:on('ready', function()
    print('Logged in as '.. client.user.username)
    ch = client:getChannel(CHANNEL_ID)
	
	if ch ~= nil and announce_hypeman_start then
		ch:send('HypeMan standing by to standby.')
	end
end)

cqbot:on('ready', function()
    print('Logged in as '.. cqbot.user.username)
		
    cqch = cqbot:getChannel(CQ_BOT_CHANNEL_ID)
	
	if cqch ~= nil and announce_hypeman_start then
		cqch:send('Negative Ghostrider, the pattern is full.')
	end
end)

--local function has_value (tab, val)
--    for index, value in ipairs(tab) do
--        if value == val then
--            return true
--        end
--    end
--
--    return false
--end

function readAll(file)
    local f = assert(io.open(file, "rb"))
    local content = f:read("*all")
    f:close()
    return content
end

client:on('messageCreate', function(message)	
	
--	if message.content == '!connect' and message.author.id == privmsgid and message.channel.guild == nil then	
--		print('Message was !connect received')
--		message.channel:send('connecting to voice comms.')
--		ConnectVoice()
--		return
--	end
	
--	if message.content == '!disconnect' and message.author.id == privmsgid and message.channel.guild == nil then
--	    message.channel:send('disconnecting from voice comms.')
--		DisconnectVoice()
--		return
--	end	
	
--	if message.author.id == privmsgid and message.channel.guild == nil then
--		print('Creating Message '..message.content)
--		CreateVoiceMp3(message.content)
--	end
		
--	if id  == CHANNEL_ID then
--		local content = message.content
--		if content == '!info' or content == '!about' or content == '!hypeman' then			
--			message.channel:send('HypeMan is an experimental Discord bot to announce Digital Combat Simulator (DCS) game events to Discord.  See https://aggressors.ca/hypeman for more information')		
--		end
--	end	
	if message.content == '!server_info' then
		local final_string = 'server_info.bat'
		os.execute(final_string)
		local str = readAll(DATA_FOLDER .. "/server_info.txt")
		message.channel:send(str)
		return
	end

	if message.content == '#boatstuff' then
		local final_string = 'boardroom.bat'
		os.execute(final_string)		
		message.channel:send {
			file = IMG_FOLDER .. "/final.jpg",
		}
	end
end)

client:run(BOT_CLIENT_ID)
cqbot:run(CQ_BOT_ID)

local s2 = dgram.createSocket('udp4')

p('PORT',PORT)
s2:bind(PORT,HOST)

-- local s1 = dgram.createSocket('udp4')
-- s1:bind(PORT,HOST)
-- s1:send('HELLO', PORT+1, '127.0.0.1')

local function starts_with(str, start)
   return str:sub(1, #start) == start
end

--    * *Name*: The player name.
--    * *Pass*: A running number counting the passes of the player
--    * *Points Final*: The final points (i.e. when the player has landed). This is the average over all previous bolters or waveoffs, if any.
--    * *Points Pass*: The points of each pass including bolters and waveoffs.
--    * *Grade*: LSO grade.
--    * *Details*: Detailed analysis of deviations within the groove.
--    * *Wire*: Trapped wire, if any.
--    * *Tgroove*: Time in the groove in seconds (not applicable during Case III).
--    * *Case*: The recovery case operations in progress during the pass.
--    * *Wind*: Wind on deck in knots during approach.
--    * *Modex*: Tail number of the player.
--    * *Airframe*: Aircraft type used in the recovery.
--    * *Carrier Type*: Type name of the carrier.
--    * *Carrier Name*: Name/alias of the carrier.
--    * *Theatre*: DCS map.
--    * *Mission Time*: Mission time at the end of the approach.
--    * *Mission Date*: Mission date in yyyy/mm/dd format.
--    * *OS Date*: Real life date from os.date(). Needs **os** to be desanitized.

local function getCaseString(mygrade)

	local caseNumber = mygrade.case
	
	if caseNumber == 1 then
		return '(CASE I)' 
	elseif caseNumber == 2 then
		return '(CASE II)' 
	elseif caseNumber == 3 then
		return '(CASE III)'
	else
		return ''
	end
end

local function getWireString(mygrade)
	local mywire = mygrade.wire
	
	if mywire == nil then
		return 'no wire'
	end
	
	if mywire == 1 then
		return '1-wire'
	elseif mywire == 2 then
		return '2-wire'
	elseif mywire == 3 then
		return '3-wire'
	elseif mywire == 4 then
		return '4-wire'
	else
		return 'no wire'
	end
end

--mygrade = {}
--mygrade.grade = '_OK_'
--mygrade.points = 3.0
--mygrade.finalscore = 2.5
--mygrade.details = 'LOL HIM XAR'
--mygrade.wire=3
--mygrade.Tgroove = 16.6
--mygrade.case = 1
--mygrade.wind= 25
--mygrade.modex = 300
--mygrade.airframe = 'F/A-18C hornet'
--mygrade.carriertype = 'CVN99'
--mygrade.carriername = 'HMCS Don Cherry'
--mygrade.theatre = 'Persian Gulf'
--mygrade.mitime = '01:02:03+1'
--mygrade.midate= '1999/03/24'
--mygrade.osdate = '2019/09/10 01:02:03'

-- this function was called wrap in quotes (wiq) because it originally wrapped
-- values in quotes.  But now it joins values with a ',' but the name was kept
local function wiq(str)
	return str..', '
end

local function addToTable(tbl,keystr, defval)

	if tbl[keystr] == nil then
		tbl[keystr] = defval
	end
	
	return tbl
end
	
local function isempty(s)
  return s == nil or s == ''
end

local function isString(s)
	--print(type(s))
	if type(s) == 'string' then
		return true
	elseif type(s) == nil then
		return true
	else
		return false
	end
end

function round2(num, numDecimalPlaces)
  if isempty(num) then
	return num
  end

  if isString(num) then

	return num
   end

  return tonumber(string.format("%." .. (numDecimalPlaces or 0) .. "f", num))
end


local function defaultGrade(mygrade)
-- This function looks at the grade table provided by AIRBOSS and fills in any of the fields
-- that might not be present
	mygrade = addToTable(mygrade,'name','') --	mygrade.name
	mygrade = addToTable(mygrade,'grade','')  -- mygrade.grade
	mygrade = addToTable(mygrade,'points','') -- mygrade.points
	mygrade = addToTable(mygrade,'finalscore','') -- mygrade.finalscore
	mygrade.finalscore = round2(mygrade.finalscore,3)
	
	mygrade = addToTable(mygrade,'details','') -- mygrade.details
	mygrade = addToTable(mygrade,'wire','') -- mygrade.wire
	mygrade = addToTable(mygrade,'Tgroove','') -- mygrade.Tgroove
	mygrade.Tgroove = round2(mygrade.Tgroove,2)
	
	mygrade = addToTable(mygrade,'case','') -- mygrade.case
	mygrade = addToTable(mygrade,'wind','') -- mygrade.wind
	mygrade = addToTable(mygrade,'modex','') -- mygrade.modex
	mygrade = addToTable(mygrade,'airframe','') -- mygrade.airframe
	mygrade = addToTable(mygrade,'carriertype','') -- mygrade.carriertype
	mygrade = addToTable(mygrade,'carriername','') -- mygrade.carriername
	mygrade = addToTable(mygrade,'theatre','') -- mygrade.theatre
	mygrade = addToTable(mygrade,'mitime','') -- mygrade.mitime
	mygrade = addToTable(mygrade,'midate','') -- mygrade.midate
	return mygrade
end

local function getCsvString(mygrade)
-- This function generates the CSV row that gets sent to google sheet.
-- Every value gets wiq'd (wrapped in quotes (a single quote) )
-- The google sheet upload is handled by a python script that uploads the CSV string
	local my_string = wiq(mygrade.name)
	my_string = my_string .. wiq( mygrade.grade)
	my_string = my_string .. wiq( mygrade.points)
	my_string = my_string .. wiq( mygrade.finalscore)
	my_string = my_string .. wiq( mygrade.details)
	my_string = my_string .. wiq( mygrade.wire)
	my_string = my_string .. wiq( mygrade.Tgroove)
	my_string = my_string .. wiq( mygrade.case)
	my_string = my_string .. wiq( mygrade.wind)
	my_string = my_string .. wiq( mygrade.modex)
	my_string = my_string .. wiq( mygrade.airframe)
	my_string = my_string .. wiq( mygrade.carriertype)
	my_string = my_string .. wiq( mygrade.carriername)
	my_string = my_string .. wiq( mygrade.theatre)
	my_string = my_string .. wiq( mygrade.mitime)
	my_string = my_string .. wiq(mygrade.midate)
	my_string = my_string .. ' Server: ' .. SERVERNAME
	--my_string = my_string .. wiq( mygrade.osdate)
	return my_string
end


-- calculate Flight Hours: wheels up - wheels down + 5 minutes, round to 0.1 hours
-- https://www.airliners.net/forum/viewtopic.php?t=774829
local function calcFlightHours(mylog)
	local flighHours = 0
	
	if mylog.trackedTime ~= nil then
		flightHours = round2(mylog.trackedTime,1)
		-- print('flight hours rounded: '..flightHours)
	end
	
	return flightHours	
end

local function getFlightLogCsvString(mylog)

	flightHours = calcFlightHours(mylog)

	print('callsign')
	local my_string = wiq(mylog.callsign)
	
	print('flightHours')
	my_string = my_string .. wiq( flightHours )
	
	print('acType')
	my_string = my_string .. wiq( mylog.acType )
	
	print('numTakeoffs')
	my_string = my_string .. wiq( mylog.numTakeoffs)
	
	print('numLandings')
	my_string = my_string .. wiq( mylog.numLandings)
	
	print('departureField')
	my_string = my_string .. wiq( mylog.departureField )
	
	print('arrivalField1')
	my_string = my_string .. wiq( mylog.arrivalField1 )
	
	print('arrivalField2')
	my_string = my_string .. wiq( mylog.arrivalField2 )
	
	print('coalition')
	my_string = my_string .. wiq( mylog.coalition )
	
	print('missionType')
	my_string = my_string .. wiq( mylog.missionType )
	
	print('ServerName')
	my_string = my_string .. wiq( SERVERNAME )
	
	print('Osdate')
	my_string = my_string .. wiq( os.date('%Y/%m/%d') )
	
	print('os time')
	my_string = my_string .. wiq( os.date('%H:%M:%S') ) 
	
	print('theatre')
	my_string = my_string .. wiq( mylog.theatre )
	
	print('dead')
	my_string = my_string .. wiq( mylog.dead )
	
	print('crash')
	my_string = my_string .. wiq( mylog.crash )
	
	print('ejected')
	my_string = my_string .. wiq( mylog.ejected )
	
	print('refueled')
	my_string = my_string .. wiq( mylog.refueled )
	
	print('humanfailure')
	my_string = my_string .. wiq( mylog.humanFailure )
	
	print('airStart')
	my_string = my_string .. wiq( mylog.airStart )
	
	print('missionEnd')
	my_string = my_string .. wiq( mylog.missionEnd )
	
	return my_string
end

local function getGradeString(mygrade)
-- This is the function that formats the grade string that will get sent to Discord reporting the grade.
-- Example: Rob, (OK), 3.5 PT, H_LUL_X _SLO_H_LUL_IM  SLOLOLULIC LOAR, 3-wire, groove time 17.0 seconds, (CASE I)
	print ('LSO Grade, '.. mygrade.name .. ' trapped, sending to Discord')
	
	local grade_string = string.gsub(mygrade.grade, '_', '\\_')
	local details_string = string.gsub(mygrade.details, '_','\\_')

	local msg_string = mygrade.name .. ', ' .. grade_string .. ', ' .. mygrade.points .. ' PT, ' .. details_string .. ', ' .. getWireString(mygrade)
	
	if mygrade.case ~= 3 then
		msg_string = msg_string .. ', ' .. mygrade.Tgroove .. ' seconds'		  
	end
	
	msg_string = msg_string .. ', ' .. mygrade.airframe .. ', ' .. getCaseString(mygrade)	

	return msg_string
end


local function savetable ( tbl, myfilename)
   local file = assert(io.open(myfilename, "w"))
   
   local tbl_json_txt = JSON:encode(tbl) 
   
   file:write(tbl_json_txt )
   file:close()
end

local function savetxt ( t )
   local file = assert(io.open(DATA_FOLDER .. "lso_table.json", "w"))
   file:write(t)
   file:close()
end

local function f(msg)

	local lua_table = JSON:decode(msg)
	savetxt(msg)
	if lua_table['messageType']  ~= nil then
		local msg_id = lua_table['messageType']
			
		if msg_id == 1 then
			-- print the message
			if ch ~= nil then
				local msg_string = lua_table['messageString']
				
				msg_string = string.gsub(msg_string, '$SERVERNAME', SERVERNAME)
				
				if msg_string ~= nil then
					ch:send(msg_string)
				end
			end
	
		elseif msg_id == 2 then
			-- AIRBOSS GRADE IS messageType = 2			
						
			if cqch ~= nil then
				-- cqch:send('MessageType = 2')
				
				lua_table = defaultGrade(lua_table)		
				local msg_string = getGradeString(lua_table)
				print(msg_string)
				--cqch:send(msg)
				cqch:send(msg_string)
				local msg2 = getCsvString(lua_table)
				local execString = "\".\\gsheet_upload.bat " .. "\"" .. msg2 .. "\"\""
				print(execString)
				io.popen(execString,'w')
				
				local execString2 = 'trapsheet.bat'
				os.execute(execString2)
				
				cqch:send {
					file = IMG_FOLDER .. "trapsheet.png",
				}				
			end

		elseif msg_id == 3 then
			-- PILOT FLIGHT TIME MESSAGE?
			print('FLIGHT LOG MESSAGE RECEIVED')

			local flightLogString = getFlightLogCsvString(lua_table)
			--local flightLogString = 'abc'
			local execString = "\".\\flightlog_upload.bat ".. "\"" .. flightLogString .. "\"\""
			print(execString)
			io.popen(execString,'w')

			--savetxt ( msg3 )			
			
		elseif msg_id == 4 then
			-- WEAPON RELEASE MESSAGE?
			
		elseif msg_id == 5 then
			-- HIT OR DAMAGE MESSAGE?
		end
	end

end

--local msg2 = "TG, (OK), 3.0 PT, F(LOLUR)X F(LOLUR)IM  (F)IC , 1-wire, groove time 22.0 seconds, (CASE I)"    
--local execString = "\".\\gsheet_upload.bat " .. "\"" .. msg2 .. "\"\""
--print(execString)
--pcall(io.popen(execString,'w'))
			
s2:on('message', function(msg, rinfo)
	-- local t = os.date()	
    p('Message received: ')
    p(msg)
    
    if ch ~= nil then
		botSendMessage = coroutine.wrap (f)
        botSendMessage(msg)
    end
	-- nilling the message here.  Somehow the message was getting appended to and growing?  not sure how or why that happened
	-- msg = nil
	-- Seemed to only be due to time acceleration in DCS?  I don't know.
end)