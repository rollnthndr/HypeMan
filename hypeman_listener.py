import logging
from logging import config
import pathlib
from config.config import APP_CONFIG, DISCORD_CONFIG

# set up the global logger
logging.config.fileConfig(
    pathlib.Path(APP_CONFIG["app"]["logging_config"]),
    disable_existing_loggers=True,
)
logging.getLogger("comprehensive")


class HypeManListener:
    def __init__(self):
        logging.debug('Initializing HypeManListener')
        self._host = APP_CONFIG["app"]["host"]
        self._port = APP_CONFIG["app"]["port"]


if __name__ == "__main__":
    # we begin....
    logging.info('HypeMan listening...')

    HypeManListener()