# Work Queue
* Task Queues main idea is to avoid doing a resource-intensive task immediately and having to wait for it to complete.
* Instead we schedule the task to be done later.

* so let's fake it by just pretending we're busy - by using the time.sleep() function

![Work queue, one producer and two consumer](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/2-RabbitMq%20Python%20Hello%20worldi.png)

auto_ack=True

python new_task.py First message.
python new_task.py Second message..
python new_task.py Third message...
python new_task.py Fourth message....
python new_task.py Fifth message.....

auto_ack=False
A timeout (30 minutes by default)is enforced on consumer delivery acknowledgement.


## Message durability
```python
channel.queue_declare(queue='hello', durable=True)
```

```python
channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                      ))
```

## Fair dispatch
* when all odd messages are heavy and even messages are light, one worker will be constantly busy and the other one will do hardly any work.''

* It doesn't look at the number of unacknowledged messages for a consumer. It just blindly dispatches every n-th message to the n-th consumer.

```python
channel.basic_qos(prefetch_count=1)
```
