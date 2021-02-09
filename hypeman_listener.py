import subprocess
import discord
import asyncio
import asyncio_dgram
import logging
import config.settings as CFG
import config.settings_discord as CFG_DISCORD
from config.logger import logger

log = logger(__name__, CFG.APP.FILE_HYPEMAN_LOG, "w", CFG.APP.DEBUG)


class AirbossHypemanBot(discord.Client):
    def __init__(
        self, client_id: str, channel_id: int, announce: bool, announce_msg: str,
        server_info_data: str, greenieboard_img: str
    ):
        super().__init__()
        self.channel = None
        self.client_id = client_id
        self.channel_id = channel_id
        self.announce = announce
        self.announce_msg = announce_msg
        self.server_info_data = server_info_data
        self.greenieboard_img = greenieboard_img

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
            log.info(f"Creating greenie board.")
            if log.level == logging.DEBUG:
                await self.channel.send(f"```Creating greenie board.```")

            # Create the greenie board and send it to discord
            await self._do_greenie_board()

        elif message.content.startswith("!server_info"):
            # call server_info.py and send resulting text to discord
            log.info("Getting server info.")
            if log.level == logging.DEBUG:
                await self.channel.send(f"```Getting server info.```")

            # Retrieve the server info and send it to discord
            await self._do_sever_info()
        else:
            pass

    async def on_error(self, event, *args, **kwargs):
        log.debug(f"Bot error - {event}\n{args}")

    async def _do_sever_info(self):
        try:
            # Check the servers and create the output txt file
            subprocess.run(["python", "server_info.py"])

            # Send the resulting txt file text to discord
            msg_text = ""

            with open(self.server_info_data) as file:
                content = file.readlines()
                for line in content:
                    msg_text += f"> {line}\n"

            # msg_text += f"`"

            await self.channel.send(msg_text)
        except Exception as e:
            log.info(f'Error - {e}')

    async def _do_greenie_board(self):
        try:
            # Build the board image
            subprocess.run(["python", "boardroom.py"])

            # build the final boardroom image
            subprocess.run(["python", "boardroom_compose.py"])
            
            # send image file to discord
            await self.channel.send(file=discord.File(self.greenieboard_img))
        except Exception as e:
            log.info(f'Error - {e}')


class HypeManListener:
    def __init__(self, host: str, port: int, bot: AirbossHypemanBot):
        self.bot = bot
        self._host = host
        self._port = port

        log.debug("Initialized HypeManListener")

    async def start_listener(self):
        """Start listening for DCS messages"""

        try:
            # bind udp server to the host/port
            stream = await asyncio_dgram.bind((self._host, self._port))
            log.info(f"Listening on {stream.sockname}")

            # main listener loop
            while 1:
                # wait to receive data
                data, remote_addr = await stream.recv()
                log.debug(f"From : {remote_addr}\tUDP received - {data.decode()!r}")
        except Exception as e:
            log.debug(f'Error - {e}')


if __name__ == "__main__":

    # Create the BOT and Listener classes
    hm_bot = AirbossHypemanBot(
        CFG_DISCORD.HYPEMAN.ID_CLIENT,
        CFG_DISCORD.HYPEMAN.ID_CHANNEL,
        CFG_DISCORD.HYPEMAN.BOT_ANNOUNCE,
        CFG_DISCORD.HYPEMAN.BOT_ANNOUNCE_MSG,
        CFG.SERVERINFO.FILE_DATA,
        CFG.GREENIEBOARD.IMAGE_BOARDROOM_FINAL
    )
    hm_listener = HypeManListener(
        CFG.APP.HOST,
        CFG.APP.PORT,
        hm_bot
    )

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

