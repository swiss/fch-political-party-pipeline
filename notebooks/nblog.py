import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent / "pipeline.log"
DATA_ERROR = 35  # zwischen WARNING (30) und ERROR (40)
logging.addLevelName(DATA_ERROR, "DATA_ERROR")

def get_logger(notebook_name: str) -> logging.Logger:
    logger = logging.getLogger(notebook_name)
    logger.setLevel(logging.INFO)

    # Verhindert doppelte Handler, wenn die Zelle mehrfach ausgeführt wird
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        ))
        logger.addHandler(handler)
        logger.propagate = False  # sonst evtl. doppelte Ausgabe in Jupyter
    return logger