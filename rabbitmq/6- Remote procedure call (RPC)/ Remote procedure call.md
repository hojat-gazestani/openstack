### Remote procedure call (RPC)
* run a function on a remote computer and wait for the result

#### Client interface
```python
fibonacci_rpc = FibonacciRpcClient()
result = fibonacci_rpc.call(4)
print("fib(4) is %r" % result)
```

### Callback queue
```python
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_publish(exchange='',
                      routing_key='rpc_queue',
                      properties=pika.BasicProperties(
                            reply_to = callback_queue,
                            ),
                      body=request)

# ... and some code to read a response message from the callback_queue ...
```

### Correlation id
* unique value for every request. Later, when we receive a message in the callback queue we'll look at this property,


### Summary

![RPC](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/8-rpc.png)

* Our RPC will work like this:
  1. When the Client starts up, it creates an anonymous exclusive callback queue.
  2. For an RPC request, the Client sends a message with two properties: **reply_to**, which is set to the callback queue and **correlation_id**, which is set to a unique value for every request.
  3. The request is sent to an **rpc_queue** queue.
  4. The RPC worker (aka: server) is waiting for requests on that queue. When a request appears, it does the job and sends a message with the result back to the Client, using the queue from the **reply_to** field.
  5. The client waits for data on the callback queue. When a message appears, it checks the **correlation_id** property. If it matches the value from the request it returns the response to the application.