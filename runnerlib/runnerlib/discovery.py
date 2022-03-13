import logging
import inspect
import re
import os
import traceback

import requests

logger = logging.getLogger(f'Server')

PORT = int(os.environ.get('PORT', 5000))

sidecar_host = os.environ.get('CONTAINER_NAME', None)
sidecar_port = int(os.environ.get('PORT', 0)) or None
sidecar_discovery_host = os.environ.get('RUNNER_DISCOVERY_HOST', None)
sidecar_discovery_port = int(os.environ.get('RUNNER_DISCOVERY_PORT', 0)) or None

assert sidecar_discovery_host is not None
assert sidecar_discovery_port is not None
assert sidecar_port is not None
assert sidecar_host is not None


class AlgorithmHandler:
    def __init__(self, function):
        self.function = function
        self.argspec = inspect.getfullargspec(function)

    def validate_body(self, body):
        # Body keys should correspond to handler args
        return sorted(body.keys()) == sorted(self.get_expected_args())

    def get_expected_args(self):
        return self.argspec.args

    def call(self, *args, **kwargs):
        self.function.__call__(*args, **kwargs)


def _register(algorithm_name):
    host = f'{sidecar_discovery_host}:{sidecar_discovery_port}/runners'
    body = {'algorithm_name': algorithm_name, 'host': f'http://{sidecar_host}:{sidecar_port}'}

    response = requests.post( host, json=body)

    response.raise_for_status()


def register():
    logger.info(f'Looking for local algorithm handlers to register at port {PORT}')

    import integration_adapter
    assert inspect.ismodule(integration_adapter)

    algorithm_handlers = inspect.getmembers(
        integration_adapter,
        predicate=lambda f: inspect.isfunction(f) and re.match(r'run_*', f.__name__)
    )

    logger.info('Found handlers', ', '.join([h[0] for h in algorithm_handlers]))

    handlers_by_algorithm = {name.split('run_')[1]: AlgorithmHandler(function) for name, function in algorithm_handlers}

    # Register algorithm with port solver
    unsuccessful = []
    for name, _ in algorithm_handlers:
        try:
            print('Registering algorithm', name)
            _register(name)
        except:
            unsuccessful.append(name)
            traceback.print_exc()

    if unsuccessful:
        print('Unable to register algorithms', ', '.join([f'`{a}`' for a in unsuccessful]))
        endpoints_registered = False
    else:
        endpoints_registered = True

    # Expose handler getter
    def get_handler(algorithm):
        return handlers_by_algorithm.get(algorithm, None)
