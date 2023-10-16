"""Logging module."""
import logging
import sys
from typing import Tuple, Dict, Any


class LoggingHandler:
    """Logging Class Handler."""
    def __init__(self, *args: Tuple, **kwargs: Dict[str, Any]):
        """Init LoggingHandler object."""
        formatter = logging.Formatter(
            '[%(asctime)s]-[%(levelname)s]-[%(filename)s::%(name)s]-[%(message)s]'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(handler)
