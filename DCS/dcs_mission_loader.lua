-- INSTRUCTIONS
-- Add this 'do script' to your mission
-- assert(loadfile("C:/HypeMan/DCS/HypeMan_Mission_Loader.lua"))()

-- This is the only script file that needs to be loaded in the DCS
-- mission to get Hypeman loaded. 
-- "HypeMan_DCS_Discord.lua" currently connects DCS to the both the
-- Discord bot and Hypeman. 
-- Mission example is just a test script
-- mission show an example of setting up the airboss to send LSOgrades
-- to Discord.



assert(loadfile("C:/HypeMan/DCS/mist.lua"))()
assert(loadfile("C:/HypeMan/DCS/Moose.lua"))()
assert(loadfile("C:/HypeMan/DCS/dcs_hypeman_connector.lua"))()
assert(loadfile("C:/HypeMan/DCS/mission_example.lua"))()