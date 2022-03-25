import pika
import sys
import os
import logging
import traceback

import requests

LOG_LEVEL = os.environ.get('LOG_LEVEL', '')
RUNNER_HOST = os.environ.get('RUNNER_HOST', 'localhost')
RUNNER_PORT = os.environ.get('RUNNER_PORT', 5000)
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'tasks')

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(levelname)s :: %(message)s')
logger = logging.getLogger('Controller')

logging.getLogger('pika').setLevel(logging.CRITICAL)


def run():
    logger.info(f'Setting up controller on queue {QUEUE_NAME}')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    def callback(channel, method, properties, body):
        try:
            logger.info('Received message, calling runner')
            headers = {'Content-Type': 'application/json'}
            response = requests.request('POST', f'http://{RUNNER_HOST}:{RUNNER_PORT}', headers=headers, data=body)

            if response.ok:
                logger.info(f'Received result from runner: {response.json()}')
            else:
                logger.error(f'Received error response from runner: {response.status_code} {response.json()}')
                # Handle error (retry/requeue/send to DLX)
        except Exception:
            error_str = traceback.format_exc()
            logger.error(f'Failed to process message: {error_str}')

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    logger.info(f'[+] Listening for messages on queue {QUEUE_NAME}')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        run()

    except pika.exceptions.AMQPConnectionError:
        logger.error('[x] Failed to connect to queue.')
        sys.exit(1)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
