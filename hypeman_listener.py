import logging
from logging import config
import pathlib
from config.config import APP_CONFIG, DISCORD_CONFIG
import discord
import asyncio

# set up the global logger at logging level set in app_settings.ini
logging.config.fileConfig(
    pathlib.Path(APP_CONFIG["app"]["logging_config"]), disable_existing_loggers=True,
)
logger = logging.getLogger(APP_CONFIG["app"]["logging_level"])


class BaseBot(discord.Client):
    async def on_ready(self):
        logger.info(f"{self.user.name} is logged onto Discord and mission ready.")


class HypeManBot(BaseBot):
    def __init__(self):
        super().__init__()

    async def on_message(self, message):
        if message.content.startswith("!server_info"):
            logger.debug("HypeMan received !server_info message.")


class AirbossBot(BaseBot):
    def __init__(self):
        super().__init__()

    async def on_message(self, message):
        if message.content.startswith("#boatstuff"):
            logger.debug("Airboss received #boatstuff message.")
            message.send("test")


class HypeManListener:
    def __init__(self):
        logger.debug("Initializing HypeManListener")
        self._host = APP_CONFIG["app"]["host"]
        self._port = APP_CONFIG["app"]["port"]
        self._announce = bool(APP_CONFIG["app"]["announce_bot_start"])
        self._bot_hypeman_client_id = DISCORD_CONFIG["hypeman"][
            "private_hypeman_client_id"
        ]
        self._bot_hypeman_channel_id = DISCORD_CONFIG["hypeman"][
            "private_hypeman_channel_id"
        ]
        self._bot_airboss_client_id = DISCORD_CONFIG["airboss"][
            "private_airboss_client_id"
        ]
        self._bot_airboss_channel_id = DISCORD_CONFIG["airboss"][
            "private_airboss_channel_id"
        ]
        self._bot_hypeman = HypeManBot()
        self._bot_airboss = AirbossBot()
        self._start_bots()

    def _start_bots(self):
        """Start Discord Bots"""

        logger.debug("Starting BOTs")
        # get the event loop and start each bot
        loop = asyncio.get_event_loop()
        loop.create_task(self._bot_hypeman.start(self._bot_hypeman_client_id))
        loop.create_task(self._bot_airboss.start(self._bot_airboss_client_id))
        try:
            loop.run_forever()
        finally:
            loop.stop()

        # if bots are to announce on Discord, send message.
        # if self._announce:
        # self._bot_hypeman.wait_until_ready()
        # logger.debug("here")


if __name__ == "__main__":
    # we begin....
    # logging.info('HypeMan listening...')

    HypeManListener()
