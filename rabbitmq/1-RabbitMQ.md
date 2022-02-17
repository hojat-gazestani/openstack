
# RabbitMQ
* is a Message broker that that implements Advanced Message Queueing Protocol (AMQP)
* AMPQ standardizes messaging using Producers, Broker and Consumers
  * producer: A program that **sends** messages. \
    ![producer symbol]() \
  * queue : Messages **stored** inside a queue. \
    ![queue symbol]() \
  * consumer:  A program that mostly waits to **receive** messages. \
    ![consumer symbol]() \
  
* Messaging increases loose coupling and scalability

* **Producer** emits messages to **exchange**
* **Consumer** receives messages from **queue**
* **Binding** connects an exchange with a queue using **binding Key**
* Exchange compare **routing key** with binding key
* Message distribution depends on **exchange type**
* Exchange types: fanout, direct, topic and headers

* **Default (nameless) exchange**
  * Special exchange created by RabbitMQ
  * Compares routing key with queue name
  * Indirectly allows sending directly to queues
  * 