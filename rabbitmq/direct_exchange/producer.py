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

rmq_connection = pika.BlockingConnection(rmq_parameters)
channel = rmq_connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message.encode('utf-8'))
print(" [x] Sent %r:%r" % (severity, message))
rmq_connection.close()
