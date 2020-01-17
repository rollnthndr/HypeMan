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
    pass


class AirbossHypemanBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.channel = None

    async def on_ready(self):
        logger.info(f"{self.user.name} is logged onto Discord and mission ready.")
        self.channel = self.get_channel(int(DISCORD_CONFIG["airboss_hypeman"]["channel_id"]))

    async def on_message(self, message):
        logger.debug(f'{message.content}')
        if message.content.startswith("!boatstuff"):
            logger.debug("Airboss Hypeman received #boatstuff message.")
            if logger.level == logging.DEBUG:
                await self.channel.send(f'```Hello from Airboss HypeMan```')

    async def on_error(self, event, *args, **kwargs):
        logger.debug(f'Error - {event}')


class HypeManListener:
    def __init__(self):
        logger.debug("Initializing HypeManListener")
        
        self._host = APP_CONFIG["app"]["host"]
        self._port = APP_CONFIG["app"]["port"]
        
        self._announce = bool(APP_CONFIG["app"]["announce_bot_start"])
        
        self._airboss_client_id = DISCORD_CONFIG["airboss_hypeman"]["client_id"]
        
        self._airboss = AirbossHypemanBot()

        self._start_listener()

    def _start_listener(self):
        """Start Discord Bots"""

        logger.debug("Starting listener")
        # get the event loop and start each bot
        loop = asyncio.get_event_loop()

        # create bot tasks
        loop.create_task(self._airboss.start(self._airboss_client_id))

        try:
            # run all tasks
            logger.debug('Starting loop')
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info('Ctl-C received, shutting down...')
            pass
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
