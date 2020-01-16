from configparser import ConfigParser, ExtendedInterpolation

# set up the global configparser
APP_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
APP_CONFIG.read("./config/app_settings.ini")

DISCORD_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
DISCORD_CONFIG.read("./config/discord_api_keys.ini")