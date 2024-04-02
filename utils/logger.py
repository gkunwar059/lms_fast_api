import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename="app.log")

handler.setFormatter(
    jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(ip_address)s %(method)s %(status_code)s"
    )
)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


# source and concept from the youtube video: link :https://www.youtube.com/watch?v=1RLFSOwpf88
