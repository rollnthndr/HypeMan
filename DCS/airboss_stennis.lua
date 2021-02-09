-- No MOOSE settings menu. Comment out this line if required.
_SETTINGS:SetPlayerMenuOff()

-- -- S-3B Recovery Tanker spawning in air.
-- local tanker=RECOVERYTANKER:New("stennis", "blue_grp_texaco")
-- tanker:SetTakeoffHot()
-- tanker:SetAltitude(10000)
-- tanker:SetRacetrackDistances(15, 10)
-- tanker:SetRadio(250)
-- tanker:SetModex(511)
-- tanker:SetTACAN(2, "TKR")
-- tanker:__Start(1)

-- -- E-2D AWACS spawning on Stennis.
-- local awacs=RECOVERYTANKER:New("stennis", "blue_grp_wizard")
-- awacs:SetTakeoffHot()
-- awacs:SetAWACS()
-- awacs:SetRadio(260)
-- awacs:SetAltitude(20000)
-- awacs:SetCallsign(CALLSIGN.AWACS.Wizard)
-- awacs:SetRacetrackDistances(30, 15)
-- awacs:SetModex(611)
-- awacs:SetTACAN(2, "WIZ")
-- awacs:__Start(1)

-- -- Rescue Helo with home base Perry class. Has to be a global object!
-- rescuehelo=RESCUEHELO:New("stennis", "blue_grp_rescuehelo")
-- rescuehelo:SetHomeBase(AIRBASE:FindByName("stennis"))
-- rescuehelo:SetTakeoffHot()
-- rescuehelo:SetModex(42)
-- rescuehelo:__Start(1)
  
-- Create AIRBOSS object.
local AirbossStennis=AIRBOSS:New("Stennis")

-- Add recovery windows:
-- Case I from 6:17 am to 2 pm.
local window1=AirbossStennis:AddRecoveryWindow( "6:17", "14:00", 1, nil, true, 25)
-- Case II with +15 degrees holding offset from 15:00 for 60 min.
local window2=AirbossStennis:AddRecoveryWindow("15:00", "16:00", 2,  15, true, 23)
-- Case III with +30 degrees holding offset from 2100 to 2200.
local window3=AirbossStennis:AddRecoveryWindow("21:00", "22:00", 3,  30, true, 21)

--Set TACAN
AirbossStennis:SetTACAN(74, "X", "STN")

-- Set folder of airboss sound files within miz file.
AirbossStennis:SetSoundfilesFolder("Airboss Soundfiles/")

-- Single carrier menu optimization.
AirbossStennis:SetMenuSingleCarrier()

-- Skipper menu.
AirbossStennis:SetMenuRecovery(30, 20, false)

-- Remove landed AI planes from flight deck.
AirbossStennis:SetDespawnOnEngineShutdown()

-- Load all saved player grades from your "Saved Games\DCS" folder (if lfs was desanitized).
AirbossStennis:Load()

-- Automatically save player results to your "Saved Games\DCS" folder each time a player get a final grade from the LSO.
AirbossStennis:SetAutoSave()

-- Enable trap sheet.
AirbossStennis:SetTrapSheet()

-- Start airboss class.
AirbossStennis:Start()


-- --- Function called when recovery tanker is started.
-- function tanker:OnAfterStart(From,Event,To)

--   -- Set recovery tanker.
--   AirbossStennis:SetRecoveryTanker(tanker)  


--   -- Use tanker as radio relay unit for LSO transmissions.
--   AirbossStennis:SetRadioRelayLSO(self:GetUnitName())
  
-- end

-- --- Function called when AWACS is started.
-- function awacs:OnAfterStart(From,Event,To)
--   -- Set AWACS.
-- --   AirbossStennis:SetRecoveryTanker(tanker)  
-- end


-- --- Function called when rescue helo is started.
-- function rescuehelo:OnAfterStart(From,Event,To)
--   -- Use rescue helo as radio relay for Marshal.
-- --   AirbossStennis:SetRadioRelayMarshal(self:GetUnitName())
-- end

--- Function called when a player gets graded by the LSO.
function AirbossStennis:OnAfterLSOGrade(From, Event, To, playerData, myGrade)
--   local PlayerData=playerData --Ops.Airboss#AIRBOSS.PlayerData
--   local Grade=grade --Ops.Airboss#AIRBOSS.LSOgrade

  myGrade.messageType = 2
  myGrade.name = playerData.name
  HypeMan.sendBotTable(myGrade)
  
--   local score=tonumber(Grade.points)
--   local name=tostring(PlayerData.name)
  
--   -- Report LSO grade to dcs.log file.
--   env.info(string.format("Player %s scored %.1f", name, score))
end