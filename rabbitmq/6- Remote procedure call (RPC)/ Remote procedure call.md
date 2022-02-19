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

![RPC]()
