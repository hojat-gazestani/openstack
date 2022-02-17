# Hello World

producer: A program that **sends** messages. \
![producer symbol]() \
queue : Messages **stored** inside a queue. \
![queue symbol]() \
consumer:  A program that mostly waits to **receive** messages. \
![consumer symbol]() \

## sender
```python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
```

<details><summary>CLICK ME</summary>
<p>

#### We can hide anything, even code!

    ```ruby
      puts "Hello World"
    ```

</p>
</details>