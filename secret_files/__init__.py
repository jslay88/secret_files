"""
secret_files, load secrets from files as Python runtime environment variables
"""
import logging
import os

from .methods import load_secret_files


__VERSION__ = "0.0.1" + os.getenv("SECRET_FILES_VERSION_TAG", "")

logging.getLogger(__name__).addHandler(logging.NullHandler())
