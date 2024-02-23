import os
import sys

from loguru import logger

log_level = os.environ.get('LOG_LEVEL', 'INFO')
log_format = """
    <level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>
    <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"""

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    level=log_level,
    format=log_format,
)
