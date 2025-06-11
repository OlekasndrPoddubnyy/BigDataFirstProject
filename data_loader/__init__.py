import logging
from data_loader.loader_registry import get_loader

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Se vuoi che anche stdout sia mostrato nei log
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

__all__ = ["get_loader"]

logger.debug("Modulo data_loader inizializzato.")