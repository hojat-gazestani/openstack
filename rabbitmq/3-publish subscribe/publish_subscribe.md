### publish/subscribe
* deliver a message to multiple consumers.

### Exchanges
* producer: application that sends messages.
* queue: buffer that stores messages. 
* consumer: application that receives messages.
* exchange: On one side it receives messages from producers and the other side it pushes them to queues.
  [exchange](exchange)
  * what to do with a message?
    * appended to a particular queue
    * appended to many queues
    * get discarded.
  * exchange types
    1. direct
    2. topic
    3. headers
    4. fanout: broadcasts all the messages it receives to all the queues it knows
```python
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
```

### Listing exchanges
```shell
sudo docker exec -it 2e  rabbitmqctl list_exchanges
```

### The default exchange
* default exchange identify by the empty string ("").
* messages are routed to the queue with the name specified by routing_key, if it exists.
```python
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
```

### Temporary queues
* let the server choose a random queue name for us.
```python
result = channel.queue_declare(queue='')
```

* once the consumer connection is closed, the queue should be deleted.
```python
result = channel.queue_declare(queue='', exclusive=True)
```

### Bindings
* Now we need to tell the exchange to send messages to our queue. 
* That relationship between exchange and a queue is called a binding
```python
channel.queue_bind(exchange='logs',
                   queue=result.method.queue)
```

* Listing bindings
```shell
sudo docker exec -it 2e rabbitmqctl list_bindings
```

