import logging
from logging import config
import pathlib
from config.config import APP_CONFIG, DISCORD_CONFIG
import discord
import asyncio
import asyncio_dgram

# set up the global logger at logging level set in app_settings.ini
logging.config.fileConfig(
    pathlib.Path(APP_CONFIG["app"]["logging_config"]), disable_existing_loggers=True,
)
if APP_CONFIG["app"]["debugging"].lower() == "true":
    logger = logging.getLogger("debug")
else:
    logger = logging.getLogger("info")


class AirbossHypemanBot(discord.Client):
    def __init__(self):
        super().__init__()
        logger.debug(f"Initializing AirbossHypemanBot")
        self.channel = None
        self.client_id = DISCORD_CONFIG["airboss_hypeman"]["client_id"]
        self.announce = APP_CONFIG["app"]["announce_bot_start"]
        self.announce_msg = APP_CONFIG["app"]["announce_bot_msg"]

    # Called when the bot has connected to discord and is ready.
    async def on_ready(self):
        # now that bot is connected to discord, get the channel it's connected to
        self.channel = self.get_channel(
            int(DISCORD_CONFIG["airboss_hypeman"]["channel_id"])
        )

        # bot will announce in discord once it's connected if set in ini file
        if str(self.announce).lower() == "true":
            await self.channel.send(f"`{self.announce_msg}`")

         logger.info(f"Discord bot ready.")

    async def on_message(self, message):
        # if message on channel is from this bot, we don't want to do
        # anything so just return.
        if message.author.id == self.user.id:
            return

        logger.debug(f"Message from Discord - {message.content}")

        # check message if it contains a command
        if message.content.startswith("!boatstuff"):
            # create and send greenie board to discord
            logger.debug(f'Creating greenie board.')
            if logger.level == logging.DEBUG:
                await self.channel.send(f"```Creating greenie board.```")

    async def on_error(self, event, *args, **kwargs):
        logger.debug(f"Bot error - {event}\n{args}")


class HypeManListener:
    def __init__(self, bot):
        logger.debug("Initializing HypeManListener")

        self.bot = bot

        self._host = APP_CONFIG["app"]["host"]
        self._port = int(APP_CONFIG["app"]["port"])

    async def start_listener(self):
        """Start Discord Bots"""

        # bind udp server to the host/port
        stream = await asyncio_dgram.bind((self._host, self._port))
        logger.info(f"Listening on {stream.sockname}")

        # main listener loop
        while 1:
            # wait to receive data
            data, remote_addr = await stream.recv()
            logger.debug(f"UDP received - {data.decode()!r}")


if __name__ == "__main__":

    hp_bot = AirbossHypemanBot()
    hm_listener = HypeManListener(hp_bot)

    # get the event main loop to run the tasks asynchronously
    loop = asyncio.get_event_loop()

    # udp server task
    loop.create_task(hm_listener.start_listener())

    # discord bot task
    loop.create_task(hm_listener.bot.start(hm_listener.bot.client_id))

    try:
        # run all tasks in infinite loop
        logger.debug("Starting listener and bot.")
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Ctl-C received, shutting down.")
    finally:
        loop.stop()

