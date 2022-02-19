### Routing
* direct only critical error messages to the log file (to save disk space), 
* while still being able to print all the log messages on the console.

### Binding
* relationship between an exchange and a queue (queue is interested in messages from this exchange.)

### Direct exchange
* Send messages to queue where routing key = binding_key

```python
channel.queue_bind(exchange=exchange_name,
                   queue=queue_name,
                   routing_key='black')
```

![Direct exchange](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/4-Direct%20Exchange.png)

### Multiple bindings

![Multiple bindings](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/5-Multiple%20bindings.png)

* In that case, the direct exchange will behave like fanout and will broadcast the message to all the matching queues.

### New log system
