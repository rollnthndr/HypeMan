import subprocess
import logging
from logging import config
from pathlib import Path
import discord
import asyncio
import asyncio_dgram
import config.settings as CFG
import config.settings_discord as CFG_DISCORD
from config.logger import logger

log = logger(__name__, CFG.APP.FILE_LOG, 'w', CFG.APP.DEBUG)

class AirbossHypemanBot(discord.Client):
    def __init__(self, client_id: str, channel_id: int, announce: bool, announce_msg: str ):
        super().__init__()
        self.channel = None
        self.client_id = client_id
        self.channel_id = channel_id
        self.announce = announce
        self.announce_msg = announce_msg

        log.debug(f"Initialized AirbossHypemanBot")

    # Called when the bot has connected to discord and is ready.
    async def on_ready(self):
        # now that bot is connected to discord, get the channel it's connected to
        self.channel = self.get_channel(self.channel_id)

        # bot will announce in discord once it's connected if set in ini file
        if self.announce == True:
            await self.channel.send(f"`{self.announce_msg}`")

        log.info(f"Discord bot ready.")

    async def on_message(self, message):
        # if message on channel is from this bot, we don't want to do
        # anything so just return.
        if message.author.id == self.user.id:
            return

        # check message if it contains a command
        if message.content.startswith("!boatstuff"):
            # create and send greenie board to discord
            log.info(f'Creating greenie board.')
            if log.level == logging.DEBUG:
                await self.channel.send(f"```Creating greenie board.```")

        elif message.content.startswith("!server_info"):
            # call server_info.py and send resulting text to discord
            log.info('Getting server info.')
            if log.level == logging.DEBUG:
                await self.channel.send(f"```Getting server info.```")

            subprocess.run(['python', 'server_info.py'])
        else:
            pass

    async def on_error(self, event, *args, **kwargs):
        log.debug(f"Bot error - {event}\n{args}")



class HypeManListener:
    def __init__(self, bot):
        self.bot = bot
        self._host = CFG.APP.HOST
        self._port = CFG.APP.PORT

        log.debug("Initialized HypeManListener")

    async def start_listener(self):
        """Start Discord Bots"""

        # bind udp server to the host/port
        stream = await asyncio_dgram.bind((self._host, self._port))
        log.info(f"Listening on {stream.sockname}")

        # main listener loop
        while 1:
            # wait to receive data
            data, remote_addr = await stream.recv()
            log.debug(f"From : {remote_addr}\tUDP received - {data.decode()!r}")


if __name__ == "__main__":

    # Create the BOT and Listener classes
    hm_bot = AirbossHypemanBot(CFG_DISCORD.HYPEMAN.ID_CLIENT,
                                CFG_DISCORD.HYPEMAN.ID_CHANNEL,
                                CFG_DISCORD.HYPEMAN.BOT_ANNOUNCE,
                                CFG_DISCORD.HYPEMAN.BOT_ANNOUNCE_MSG)
    hm_listener = HypeManListener(hm_bot)

    # get the event main loop to run the tasks asynchronously
    loop = asyncio.get_event_loop()

    # udp server task
    loop.create_task(hm_listener.start_listener())

    # discord bot task
    loop.create_task(hm_listener.bot.start(hm_listener.bot.client_id))

    try:
        # begin running the listener and bot
        log.debug("Starting listener and bot.")
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("Ctl-C received, shutting down.")
    finally:
        loop.stop()

