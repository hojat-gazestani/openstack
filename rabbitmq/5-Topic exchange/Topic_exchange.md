### Topic exchange
* can't have an arbitrary routing_key - it must be a list of words, delimited by dots. 
* The words can be anything, but usually they specify some features connected to the message.

* like direct one - a message sent with a particular routing key will be delivered to all the queues that are bound with a matching binding key
* However there are two important special cases for binding keys:
  1. \* (star) can substitute for exactly one word.
  2. \# (hash) can substitute for zero or more words.

![Topic exchange]() 