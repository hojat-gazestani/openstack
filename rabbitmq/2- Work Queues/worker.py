import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.queue_declare(queue='not_dur')
#print(' [*] Waiting for messages. To exit press CTRL+C')

channel.queue_bind(exchange='logs', queue='not_dur')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    #print(" [x] Received %r" % body.decode())
    #time.sleep(body.count(b'.'))
    #print(" [x] Done")
    #ch.basic_ack(delivery_tag=method.delivery_tag)


#channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='not_dur', on_message_callback=callback)

channel.start_consuming()
