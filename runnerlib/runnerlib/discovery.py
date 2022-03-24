import logging
import inspect
import re
import traceback

import requests

from .settings import host, runner_discovery_uri

logger = logging.getLogger(f'Discovery')


handlers_by_algorithm = {}


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


def _register_single(algorithm_name):
    body = {'algorithm': algorithm_name, 'host': host}

    response = requests.post(runner_discovery_uri, json=body)

    response.raise_for_status()


def register_all():
    logger.info(f'Loading runner adapter...')

    import runner_adapter

    logger.info(f'Loading runner adapter members...')

    algorithm_handlers = inspect.getmembers(
        runner_adapter,
        predicate=lambda f: inspect.isfunction(f) and re.match(r'run_*', f.__name__)
    )

    print('potato')

    logger.info(f'Found handlers: {", ".join([h[0] for h in algorithm_handlers])}')

    global handlers_by_algorithm
    handlers_by_algorithm = {name.split('run_')[1]: AlgorithmHandler(function) for name, function in algorithm_handlers}

    # Register algorithm with runner discovery
    unsuccessful = []
    for name in handlers_by_algorithm:
        try:
            print('Registering algorithm', name)
            _register_single(name)
        except:
            unsuccessful.append(name)
            traceback.print_exc()

    if unsuccessful:
        print('Unable to register algorithms', ', '.join([f'`{a}`' for a in unsuccessful]))


# Expose handler getter
def get_handler(algorithm):
    return handlers_by_algorithm.get(algorithm, None)
