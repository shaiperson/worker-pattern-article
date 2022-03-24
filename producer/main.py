import json
import sys

import pika

usage_string = 'python main.py <algorithm> <payload_str>'

assert len(sys.argv) > 2, f'Please pass algorithm to run and payload to run it on. Usage: {usage_string}'

algorithm = sys.argv[1]
payload = sys.argv[2]

# Make sure RabbitMQ container is running with default ports mapped

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='tasks')

body = dict(algorithm=algorithm, payload=json.loads(payload))

print('Submitting body', body)

channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps(body))

