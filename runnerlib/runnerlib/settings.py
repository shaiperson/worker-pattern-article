import os

CONTAINER_NAME = os.environ.get('CONTAINER_NAME', None)
PORT = int(os.environ.get('PORT', 0)) or None
RUNNER_DISCOVERY_CONTAINER_NAME = os.environ.get('RUNNER_DISCOVERY_CONTAINER_NAME', None)
RUNNER_DISCOVERY_PORT = int(os.environ.get('RUNNER_DISCOVERY_PORT', 0)) or None

assert CONTAINER_NAME is not None
assert PORT is not None
assert RUNNER_DISCOVERY_CONTAINER_NAME is not None
assert RUNNER_DISCOVERY_PORT is not None

host = f'http://{CONTAINER_NAME}:{PORT}'
runner_discovery_uri = f'http://{RUNNER_DISCOVERY_CONTAINER_NAME}:{RUNNER_DISCOVERY_PORT}'
