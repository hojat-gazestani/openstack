import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

n = 30
result = channel.queue_declare(queue='send_q' )
#result = channel.queue_declare(queue='send_q', exclusive=True)
callback_queue = result.method.queue

response = None
corr_id = 'hojat'
channel.basic_publish(
    exchange='',
    routing_key='rpc_queue',
    properties=pika.BasicProperties(
        reply_to=callback_queue,
        correlation_id=corr_id,
    ),
    body=str(n))

def on_response(ch, method, props, body):
    global response
    if corr_id == props.correlation_id:
        response = body
        

channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

while response is None:
    connection.process_data_events()
resp = int(response)

print(resp)
