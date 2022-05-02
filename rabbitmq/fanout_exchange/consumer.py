import os
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

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='fanout_logs', queue=queue_name)


def callback(ch, method, properties, body):
    print(" [x] %r" % body.decode())


print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
