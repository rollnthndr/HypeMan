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

class HypeManBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.channel = None

    async def on_ready(self):
        logger.info(f"{self.user.name} is logged onto Discord and mission ready.")
        self.channel = self.get_channel(int(DISCORD_CONFIG["hypeman"]["channel_id"]))

    async def on_message(self, message):
        if message.content.startswith("!server_info"):
            logger.debug("HypeMan received !server_info message.")
            if logger.level == logging.DEBUG:
                await self.channel.send(f'```Hello from HypeMan```')

    async def on_error(self, event, *args, **kwargs):
        logger.debug(f'{event}')


class AirbossBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.channel = None

    async def on_ready(self):
        logger.info(f"{self.user.name} is logged onto Discord and mission ready.")
        self.channel = self.get_channel(int(DISCORD_CONFIG["airboss"]["channel_id"]))

    async def on_message(self, message):
        if message.content.startswith("#boatstuff"):
            logger.debug("Airboss received #boatstuff message.")
            if logger.level == logging.DEBUG:
                await self.channel.send(f'```Hello from Airboss```')

    async def on_error(self, event, *args, **kwargs):
        logger.debug(f'{event}')


class UdpServer(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logger.debug(f'Received UDP msg - {data}')


class HypeManListener:
    def __init__(self):
        logger.debug("Initializing HypeManListener")
        
        self._host = APP_CONFIG["app"]["host"]
        self._port = APP_CONFIG["app"]["port"]
        
        self._announce = bool(APP_CONFIG["app"]["announce_bot_start"])
        
        self._bot_hypeman_client_id = DISCORD_CONFIG["hypeman"]["client_id"]
        self._bot_airboss_client_id = DISCORD_CONFIG["airboss"]["client_id"]
        
        self._bot_hypeman = HypeManBot()
        self._bot_airboss = AirbossBot()

        self._udp_server = UdpServer()

        self._start_listener()

    def _start_listener(self):
        """Start Discord Bots"""

        logger.debug("Starting listener")
        # get the event loop and start each bot
        loop = asyncio.get_event_loop()

        # create bot tasks
        loop.create_task(self._bot_hypeman.start(self._bot_hypeman_client_id))
        loop.create_task(self._bot_airboss.start(self._bot_airboss_client_id))

        # create udp server task
        loop.create_datagram_endpoint(UdpServer,local_addr=(f'{self._host}',int(self._port)))

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
