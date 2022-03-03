import json
import sys

import pika

usage_string = 'python main.py <meme_image_url>'

assert len(sys.argv) > 1, f'Please pass URL of meme image to analyze. Usage: {usage_string}'

url_arg = sys.argv[1]

# Make sure RabbitMQ container is running with default ports mapped

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='tasks')

channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps({"url": url_arg}))

