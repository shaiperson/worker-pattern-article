import pika
import json

# Make sure RabbitMQ container is running with default ports mapped

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='tasks')

channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps({"url": "https://i.redd.it/if3ldk2w2j841.jpg"}))

