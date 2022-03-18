import pika
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

n = 30
response = None
corr_id = str(uuid.uuid4())

channel.basic_consume(queue=callback_queue, on_message_callback=on_resonse, auto_ack=True)

channel.basic_publish(exchange='',
 routing_key='rpc_queue',
 properties=pika.BasicProperties(replay_to=callback_queue, correlation_id=corr_id),
 body=str(n))
