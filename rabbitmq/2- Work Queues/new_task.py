import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.queue_declare(queue='')

message = ' '.join(sys.argv[1:]) or "Hello World......"
channel.basic_publish(
    exchange='logs',
    routing_key='not_dur',
    body=message,
    )


#print(" [x] Sent %r" % message)
#connection.close()
