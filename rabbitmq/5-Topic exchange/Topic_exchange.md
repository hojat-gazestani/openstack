### Topic exchange
* can't have an arbitrary routing_key - it must be a list of words, delimited by dots. 
* The words can be anything, but usually they specify some features connected to the message.

* like direct one - a message sent with a particular routing key will be delivered to all the queues that are bound with a matching binding key
* However there are two important special cases for binding keys:
  1. \* (star) can substitute for exactly one word.
  2. \# (hash) can substitute for zero or more words.

![Topic exchange](https://github.com/hojat-gazestani/openstack/blob/main/rabbitmq/pic/7-topic%20exchange.png)

* Q1
  * quick.orange.fox
* Q2
  * lazy.brown.fox
  * lazy.pink.rabbit
  * lazy.orange.male.rabbit
* Both
  * quick.orange.rabbit
  * lazy.orange.elephant
* discarded
  * quick.orange.male.rabbit

### To receive all the logs run:
```shell
python receive_logs_topic.py "#"
```

### To receive all logs from the facility "kern":
```shell
python receive_logs_topic.py "kern.*"
```

### Or if you want to hear only about "critical" logs:
````shell
python receive_logs_topic.py "*.critical"
````

### You can create multiple bindings:
```shell
python receive_logs_topic.py "kern.*" "*.critical"
```

### And to emit a log with a routing key "kern.critical" type:
```shell
python emit_log_topic.py "kern.critical" "A critical kernel error"
```