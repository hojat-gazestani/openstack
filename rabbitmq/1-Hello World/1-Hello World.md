# 1-Hello World

![A producer and consumer](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/1-%20running%20rabbitmq%20in%20docker.png)

## Install Python client RabbitMQ libraries 
```shell
python -m pip install pika --upgrade
```

### producer
```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
```

### consumer
```shell
sudo rabbitmqctl list_queues
```

```python
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

channel.start_consuming()
```