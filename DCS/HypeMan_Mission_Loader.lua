-- INSTRUCTIONS
-- Add this 'do script' to your mission
-- assert(loadfile("C:/HypeMan/DCS/HypeMan_Mission_Loader.lua"))()

-- This is the only script file that needs to be loaded in the DCS
-- mission. It will automatically load required modules.

assert(loadfile("C:/HypeMan/DCS/mist.lua"))()
assert(loadfile("C:/HypeMan/DCS/Moose.lua"))()
assert(loadfile("C:/HypeMan/DCS/HypeMan_DCS_Discord.lua"))()
assert(loadfile("C:/HypeMan/DCS/airboss_stennis.lua"))()