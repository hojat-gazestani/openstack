
import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                     properties=pika.BasicProperties(
                        delivery_mode  = pika.spec.PERSISTENT_DELIVERY_MODE
                     ))
print(" [x] Sent %r" % message)
connection.close()
