import logging

from settings import settings

log_level = getattr(logging, settings.log_level_name, 'DEBUG')
logging.basicConfig(level=log_level, format='%(levelname)s :: %(message)s')
