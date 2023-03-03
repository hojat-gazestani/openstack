# Simple network on python and mininet



### Starting Ryu controller

* Before starting Ryu controller it is reqiure to run a controller

```bash
ubuntu@sdnhubvm:~/ryu[19:49] (master)$ ./bin/ryu-manager --verbose ./ryu/app/simple_switch_13.py
loading app ./ryu/app/simple_switch_13.py
loading app ryu.controller.ofp_handler
instantiating app ./ryu/app/simple_switch_13.py of SimpleSwitch13
```



## Running mininet on Python

* vim SimpleNetwork.py

```py
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI

net = Mininet()

# Add switch and hosts
net.addSwitch('s1')
h1 = net.addHost('h1')
h2 = net.addHost('h2')

# Add links
net.addLink('h1', 'h2')
net.addLink('h2', 'h1')

# Add controller
c1 = RemoteController('c1', ip='127.0.0.1', port=6633)
net.addController(c1)

net.build()
net.start()
CLI(net)
# net
# nodes
# exit
net.stop()

```

