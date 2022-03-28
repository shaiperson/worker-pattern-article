import os
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', '')

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(levelname)s :: [%(name)s] :: %(message)s')

logging.getLogger('uvicorn').setLevel(logging.WARN)
