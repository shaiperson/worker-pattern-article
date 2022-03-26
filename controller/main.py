import pika
import sys
import os
import logging
import json
import traceback

import requests

LOG_LEVEL = os.environ.get('LOG_LEVEL', '')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'tasks')
RUNNER_DISCOVERY_CONTAINER_NAME = os.environ.get('RUNNER_DISCOVERY_CONTAINER_NAME')
RUNNER_DISCOVERY_PORT = os.environ.get('RUNNER_DISCOVERY_PORT')
assert RUNNER_DISCOVERY_CONTAINER_NAME
assert RUNNER_DISCOVERY_PORT
runner_discovery_uri = f'http://{RUNNER_DISCOVERY_CONTAINER_NAME}:{RUNNER_DISCOVERY_PORT}'

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(levelname)s :: %(message)s')
logger = logging.getLogger('Controller')

logging.getLogger('pika').setLevel(logging.CRITICAL)


def get_runner_registry():
    return requests.request('GET', runner_discovery_uri).json()


def run(runner_registry):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    def callback(channel, method, properties, body_raw):
        try:
            body = json.loads(body_raw)
            logger.info(f'Received message {body}')

            assert 'algorithm' in body
            assert 'payload' in body

            algorithm = body['algorithm']
            payload = body['payload']

            assert algorithm in runner_registry

            runner_uri = f'{runner_registry[algorithm]}/run/{algorithm}'

            logger.info(f'Calling runner on {runner_uri}')

            headers = {'Content-Type': 'application/json'}
            response = requests.request('POST', runner_uri, headers=headers, data=json.dumps(payload))

            if response.ok:
                logger.info(f'Received result from runner: {response.json()}')
            else:
                logger.error(f'[x] Received error response from runner: {response.status_code} {response.content.decode()}')
                # Handle error (retry/requeue/send to DLX)
        except:
            traceback.print_exc()
            # Handle error (retry/requeue/send to DLX)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    logger.info(f'[+] Listening for messages on queue {QUEUE_NAME}')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        logger.info('Requesting runner registry')
        runner_registry = get_runner_registry()

        logger.info(f'Obtained runner registry: {runner_registry}')
        logger.info(f'Setting up controller on queue {QUEUE_NAME}')

        run(runner_registry)

    except pika.exceptions.AMQPConnectionError:
        logger.error('[x] Failed to connect to queue.')
        sys.exit(1)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
