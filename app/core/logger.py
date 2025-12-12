import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",  # ⬅️ Save logs in this file
    filemode="a"          # Append to file instead of overwriting
)

logger = logging.getLogger("app")
