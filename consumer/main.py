import pika
import sys
import os
import logging

import requests

LOG_LEVEL = os.environ.get('LOG_LEVEL', '')
SIDECAR_HOST = os.environ.get('SIDECAR_HOST', 'localhost')
SIDECAR_PORT = os.environ.get('SIDECAR_PORT', 5000)
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'default_queue')

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(asctime)s :: %(levelname)s :: %(message)s')
logger = logging.getLogger('Consumer')


def run():
    logger.info('Setting up consumer on queue {}'.format(QUEUE_NAME))

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='tasks')

    def callback(channel, method, properties, body):
        logger.info('Received message, calling sidecar')
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", 'http://{}:{}'.format(SIDECAR_HOST, SIDECAR_PORT), headers=headers, data=body)

        if response.ok:
            logger.info(f'Received result from sidecar: {response.json()}')
        else:
            logger.error(f'Received error response from sidecar: {response.status_code} {response.json()}')
            # Handle error (retry/requeue/send to DLX)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    logger.info('Listening for messages on queue'.format(QUEUE_NAME))
    channel.start_consuming()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
