import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='topic')

message = ' '.join(sys.argv[1:]) or "info: This is information"
channel.basic_publish(exchange='logs', routing_key='info.test', body=message)
channel.basic_publish(exchange='logs', routing_key='info.test.one', body=message)
print(" [x] Sent %r" % message)

connection.close()
