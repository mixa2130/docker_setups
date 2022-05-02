import os
import sys
import pika
from dotenv import load_dotenv

load_dotenv()
credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'))
rmq_parameters = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=credentials
)

connection = pika.BlockingConnection(rmq_parameters)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
print(routing_key)
message = ' '.join(sys.argv[2:]) or 'Hello World!'.encode('utf-8')
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
