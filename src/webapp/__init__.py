import logging

from . import server

logger = logging.getLogger("webapp")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logfile.log")
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Start Flask server
app = server.create_app()