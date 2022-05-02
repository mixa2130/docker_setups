"""
Broadcasts all the messages it receives to all the queues it knows
"""
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

channel.exchange_declare(exchange='fanout_logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# Routing key will be ignored
channel.basic_publish(exchange='fanout_logs', routing_key='', body=message.encode('utf-8'))
print(" [x] Sent %r" % message)
connection.close()
