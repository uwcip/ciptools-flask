import importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__)
except importlib_metadata.PackageNotFoundError:
    __version__ = "0.0.0"

import logging

logger = logging.getLogger(__name__)
