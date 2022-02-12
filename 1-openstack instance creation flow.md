
- [What is REST](#What-is-REST)

### What is REST?

* The Characteristics of a REST system are defined by six design rules:

* Client-Server: 
  * There should be a separation between the server that offers a service, and the client that consumes it.
* Stateless: 
  * Each request from a client must contain all the information required by the server to carry out the request. in other words, the server cannot store inofrmation provided by the client in one request and use it in another request.
* Cacheable: 
  * The server must indicate to the client if requests can be cached or not.
* Layerdd Systemc:
  * Communication between a client and a server should be standardized in such a way that allows intermediaries to respond to requests instead of the end server. without the client having to do anything different.
* Uniform interface: 
  * The method of communication between a client and a server must be uniform.
* Code no demand: Server can provide executable code or scripts for clients to execute in their context . This constraint is the only one that is optional.

* Rest Method:
  * GET
  * GET
  * POST
  * PUT
  * DELETE

* RabbitMQ/QPID - Everything is a message
  * Each message is stateless
  * Consumers craete queues; the buffer message for push to co
  * Queues are stateful, ordered, a be persistent, transient, private exchanges are stateless routing 
  * Consumers tell queues to bind named exchanges; each binding pattern e.g: "tony" or "*.ibm.*"
  * Producers send messages to exchange with a routing key e.g. "tony", 

![alt text](1)

* openstack components
  * Each of the components interact using Messaging API.
  * Each Service, may have multiple internal services, such as scheduler, that also are Part of complete message flow.

![alt text](2)

* How to watch the movement
  * Log, log and log

* Best practice - Log management
  * Logstash with Kibana
  * ElasticSearch

* Nova Messaging Flow
  * ![alt text](3)

Request Flow Provisioning instance in Openstack
-----------------------------------------------
### 1- Dashboard/CLI Get User Cerds from Keystone
      Dashboard or CLI get the user credential and does the REST call to Keystone for authentication.

### 2- Keystone authenticates and sends back token
    Keystone authenticate the credentials and generate & send back auth-token which will be used for sending request to other components through REST call.

### 3- UI convert instance request to Nova API
    Dashboard or CLI convert the new instance request specified in 'Lanch instance' or 'nova-boot' from to REST API request and send it to nova-api.

### 4- Nova Validate with keystone
    Nova-api receive the request and sends request for validation auth-token and access permission to keystone.

### 5- Keystone validates Token.
    Keystone validate the token and sends update auth headers with roles and permissions.

### 6- Nova-API interacts with the Nova Database
    Nova-api interacts wiht nova-database.

### 7- Initial Entry first appears in DB
    Create initial entry for new instance.

### 8- Nova-API sends request to scheduler
    Nova-api sends the rpc.call request to nova-scheduler.
    RPC calls are visable via rabbitmq management interface or rabbitmqctl list_queues

### 9- Nova Schedule Picks Request form Q.
    Nova-scheduler picks the request from the queue.

### 10- Nova Scheduler finds the host.
    Nova-scheduler interacts with nova-database to find an appropriate host via filtering and weighing.
    Scheduling can go from simple to very complex. Typically this has a lot of customer specific customization. Highly likely to be a problematic area depending on customer.
    ![alt text](nova scheduling)

### 11- Nova Scheduler sends the replay
    Nova scheduler returns the appropriate host ID after the filtering and weighting.

### 12- Nova Scheduler asks Nova-Compute for Launch Instance.
    Nova-scheduler sends the rpc.cast request to nova-compute for 'launching instance' on appropriate host.
    Nova compute Service running on every compute node.

### 13- Nova Compute Picks up request.
    Nova compute picks up request from queue.
    This is area where you could have communication problems between nodes.

### 14- Nova-Compute request info from Nova-conductor
    Nova-compute send the rcp.call request to nova-conductor to fetch hte instance information such as host ID and flavor (RAM, CPU, Disk)
    Nova conductor is a Database Proxy to increase security.

### 15- Nova-Conductor picks request from Queue
    Nova-conductor picks the request from the queue.
    You can run multiple instance of nova-conductor on different machines as needed for scaling purposes.

### 16- Nova-Conductor interacts with DB
    Nova-conductor interacts with database.
    Nova-conductor is expected to grow in functionality to off-load long running tasks in futures releases.

### 17- Nova-Conductor returns instance info
    Nova-conductor returns instance info via queue.

### 18- Nova-Compute picks up the response
    Nova-compute picks the response from queue.
    Good example of where you need to see logs from two different hosts.

### 19- Nova-Compute gets image from Glance
    Nova-compute does the REST call by passing auth-token to glance-api to get the image URL by Image ID from glance and upload instance form image storage.

### 20- Glance-API validates auth-token
    Glance-api validates the auth-token with keystone.
    Keystone is used to validate requests from the majority of openstack services, so it's fast response is important to overall performance.

### 21- Nova-Compute gets Metadata
    Nova-compute get the image metadata.

### 22- Nova-Compute ask Neutron to allocate Net
    Nova-compute does the REST-call passing auth-token ot neutron API to allocate and configure the network such that instance gets the IP address.

### 23- Neutron-Server validates with Keystone
    Nuetron-server validates the auth-token with keystone.

### 24- Neutron returns network info to Nova-Compute
    Nova-Compute gets the network info.

### 25- Nova-Compute gets volumes from Cinder
    Nova-Compute does the REST call by passing auth-token to Volume API to attach volume to instance.

### 26- Cinder validates request with Keystone
    Cinder-API validates the auth-token with keystone.

### 27- Nova-Compute gets block storage info
    Nova-compute gets the block storage info.

### 28- Nova-Compute calss Hypervosir
    Nova-compute generates data for hypervisor driver and executes request on Hypervisor( Via libvirt or API)

### Flow - State to step

| status  |         Task         | Power State | Steps
|:----: |:--------------------:|:-----------:|:----: |
| Build   |      Scheduling      |    None     | 3-12
| Build   |      Networking      |    None     | 22-24
| Build   | Block_device_Mapping |    None     | 25-27
| Build   |       spawing        |    None     | 28
| Build   |         None         |   Running   | 





