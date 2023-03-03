## Starting nodes on mininet
```bash
ubuntu@sdnhubvm:~[11:43]$ sudo mn --top single,3 --mac --controller remote --switch ovsk
*** Creating network
*** Adding controller
Unable to contact the remote controller at 127.0.0.1:6633
*** Adding hosts:
h1 h2 h3 
*** Adding switches:
s1 
*** Adding links:
(h1, s1) (h2, s1) (h3, s1) 
*** Configuring hosts
h1 h2 h3 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
*** Starting CLI:

mininet>  links
h1-eth0<->s1-eth1 (OK OK)
h2-eth0<->s1-eth2 (OK OK)
h3-eth0<->s1-eth3 (OK OK)

mininet> nodes
available nodes are: 
c0 h1 h2 h3 s1
```
### No connection without controller
```bash
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
^C
--- 10.0.0.2 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2001ms
```


## Runnning Ryu controller
```bash
ubuntu@sdnhubvm:~/ryu[19:44] (master)$ pwd
/home/ubuntu/ryu
ubuntu@sdnhubvm:~/ryu[19:44] (master)$ ./bin/ryu-manager --verbose ./ryu/app/simple_switch_13.py
```


### Connection using controller

```bash
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=25.4 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.591 ms
^C
--- 10.0.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.591/13.036/25.482/12.446 ms
```



### control plane on controller

```bash
EVENT ofp_event->SimpleSwitch13 EventOFPPacketIn
packet in 1 00:00:00:00:00:01 ff:ff:ff:ff:ff:ff 1
EVENT ofp_event->SimpleSwitch13 EventOFPPacketIn
packet in 1 00:00:00:00:00:02 00:00:00:00:00:01 2
EVENT ofp_event->SimpleSwitch13 EventOFPPacketIn
packet in 1 00:00:00:00:00:01 00:00:00:00:00:02 1
```



## Stop Ryu and start POX

* Before starting POX h1 has connection with h2 becuase controll plan existed but can not ping h3 becuase there is no any controller also any dataplane

```bash
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=1.19 ms
^C
--- 10.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.193/1.193/1.193/0.000 ms
mininet> h1 ping h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
^C
--- 10.0.0.3 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 999ms

mininet> 
```

* Starting a new controller 

```bash
ubuntu@sdnhubvm:~/pox[19:38] (eel)$ pwd
/home/ubuntu/pox
ubuntu@sdnhubvm:~/pox[19:49] (eel)$ ./pox.py forwarding.l3_learn
```

* Create a conection from h1 to h3

```bash
mininet> h1 ping h3
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=47.3 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.370 ms
64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.144 ms
64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.065 ms
64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.023 ms
64 bytes from 10.0.0.3: icmp_seq=6 ttl=64 time=0.161 ms
64 bytes from 10.0.0.3: icmp_seq=7 ttl=64 time=0.351 ms
64 bytes from 10.0.0.3: icmp_seq=8 ttl=64 time=0.146 ms
64 bytes from 10.0.0.3: icmp_seq=9 ttl=64 time=0.135 ms
64 bytes from 10.0.0.3: icmp_seq=10 ttl=64 time=0.160 ms
64 bytes from 10.0.0.3: icmp_seq=11 ttl=64 time=0.149 ms
^C
--- 10.0.0.3 ping statistics ---
11 packets transmitted, 11 received, 0% packet loss, time 10003ms
rtt min/avg/max/mdev = 0.023/4.458/47.344/13.562 ms
mininet> 

```



### Info on mininet

```bash


mininet> dump
<Host h1: h1-eth0:10.0.0.1 pid=3583> 
<Host h2: h2-eth0:10.0.0.2 pid=3591> 
<Host h3: h3-eth0:10.0.0.3 pid=3596> 
<OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None,s1-eth3:None pid=3604> 
<RemoteController c0: 127.0.0.1:6633 pid=3577> 
mininet> h1 ifconfig -a
h1-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:01  
          inet addr:10.0.0.1  Bcast:10.255.255.255  Mask:255.0.0.0
          inet6 addr: fe80::200:ff:fe00:1/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:18 errors:0 dropped:0 overruns:0 frame:0
          TX packets:28 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1404 (1.4 KB)  TX bytes:1872 (1.8 KB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:7 errors:0 dropped:0 overruns:0 frame:0
          TX packets:7 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:784 (784.0 B)  TX bytes:784 (784.0 B)

mininet> s1 ifconfig -a
docker0   Link encap:Ethernet  HWaddr 02:42:4b:81:1d:0f  
          inet addr:172.17.42.1  Bcast:0.0.0.0  Mask:255.255.0.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

eth0      Link encap:Ethernet  HWaddr 08:00:27:c0:d6:60  
          inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fec0:d660/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:708 errors:0 dropped:0 overruns:0 frame:0
          TX packets:687 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:184146 (184.1 KB)  TX bytes:298616 (298.6 KB)

eth1      Link encap:Ethernet  HWaddr 08:00:27:ee:a7:86  
          inet addr:192.168.56.101  Bcast:192.168.56.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:feee:a786/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:17084 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13979 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:3424322 (3.4 MB)  TX bytes:5950309 (5.9 MB)

eth2      Link encap:Ethernet  HWaddr 08:00:27:2c:04:7b  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

eth3      Link encap:Ethernet  HWaddr 08:00:27:77:7f:49  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:30607 errors:0 dropped:0 overruns:0 frame:0
          TX packets:30607 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:7073534 (7.0 MB)  TX bytes:7073534 (7.0 MB)

ovs-system Link encap:Ethernet  HWaddr d2:45:6d:19:e0:27  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

s1        Link encap:Ethernet  HWaddr b2:f5:70:11:fa:4a  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:3 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

s1-eth1   Link encap:Ethernet  HWaddr 46:ab:95:24:86:6e  
          inet6 addr: fe80::44ab:95ff:fe24:866e/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:28 errors:0 dropped:0 overruns:0 frame:0
          TX packets:18 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1872 (1.8 KB)  TX bytes:1404 (1.4 KB)

s1-eth2   Link encap:Ethernet  HWaddr fe:ae:8f:39:1c:9a  
          inet6 addr: fe80::fcae:8fff:fe39:1c9a/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:17 errors:0 dropped:0 overruns:0 frame:0
          TX packets:18 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1354 (1.3 KB)  TX bytes:1348 (1.3 KB)

s1-eth3   Link encap:Ethernet  HWaddr 6e:68:3b:e1:d8:5c  
          inet6 addr: fe80::6c68:3bff:fee1:d85c/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:12 errors:0 dropped:0 overruns:0 frame:0
          TX packets:12 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:920 (920.0 B)  TX bytes:872 (872.0 B)

mininet> help

Documented commands (type help <topic>):
========================================

EOF    gterm  iperfudp  nodes        pingpair      py      switch
dpctl  help   link      noecho       pingpairfull  quit    time  
dump   intfs  links     pingall      ports         sh      x     
exit   iperf  net       pingallfull  px            source  xterm 

You may also send a command to a node using:
  <node> command {args}
For example:
  mininet> h1 ifconfig

The interpreter automatically substitutes IP addresses
for node names when a node is the first arg, so commands
like
  mininet> h2 ping h3
should work.

Some character-oriented interactive commands require
noecho:
  mininet> noecho h2 vi foo.py
However, starting up an xterm/gterm is generally better:
  mininet> xterm h2

mininet> 
```

