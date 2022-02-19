import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='direct')

message = ' '.join(sys.argv[1:]) or "error: This is an error"
channel.basic_publish(exchange='logs', routing_key='error', body=message)
print(" [x] Sent %r" % message)
connection.close()
