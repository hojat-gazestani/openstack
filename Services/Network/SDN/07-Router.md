## Router

![Scenario](https://link/to/pic)

```bash
sudo mn --top linear,2 --mac --switch ovsk,protocls=OpenFlow13 --controller remote

mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s2-eth1
s1 lo:  s1-eth1:h1-eth0 s1-eth2:s2-eth2
s2 lo:  s2-eth1:h2-eth0 s2-eth2:s1-eth2
c0

```

* Or you can do
```bash
sudo ovs-vsctl set Bridge s1 protocol=OpenFlow13
sudo ovs-vsctl set Bridge s2 protocol=OpenFlow13
```

* The result
```bash
sudo ovs-vsctl show
873c293e-912d-4067-82ad-d1116d2ad39f
    Bridge "s2"
        Controller "ptcp:6635"
        Controller "tcp:127.0.0.1:6633"
        fail_mode: secure
        Port "s2-eth2"
            Interface "s2-eth2"
        Port "s2"
            Interface "s2"
                type: internal
        Port "s2-eth1"
            Interface "s2-eth1"
    Bridge "s1"
        Controller "tcp:127.0.0.1:6633"
        Controller "ptcp:6634"
        fail_mode: secure
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1"
            Interface "s1"
                type: internal
    ovs_version: "2.3.90"
```

* Changing hosts IP address
```bash
mininet> h1 ifconfig
h1-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:01  
          inet addr:10.0.0.1  Bcast:10.255.255.255  Mask:255.0.0.0
          
mininet> h1 ip addr del 10.0.0.1/8 dev h1-eth0
mininet> h1 ip addr add 192.168.10.10/24 dev h1-eth0
mininet> h1 ifconfig
h1-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:01  
          inet addr:192.168.10.10  Bcast:0.0.0.0  Mask:255.255.255.0
          
mininet> h2 ip addr add 10.0.0.2/8 dev h2-eth0
mininet> h2 ip addr add 192.168.20.10/24 dev h2-eth0
mininet> h2 ifconfig
h2-eth0   Link encap:Ethernet  HWaddr 00:00:00:00:00:02  
          inet addr:192.168.20.10  Bcast:0.0.0.0  Mask:255.255.255.0
          
mininet> h1 route add default gw 192.168.10.1
mininet> h1 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.10.1    0.0.0.0         UG    0      0        0 h1-eth0
192.168.10.0    0.0.0.0         255.255.255.0   U     0      0        0 h1-eth0

mininet> h2 route add default gw 192.168.20.1
mininet> h2 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.20.1    0.0.0.0         UG    0      0        0 h2-eth0
192.168.20.0    0.0.0.0         255.255.255.0   U     0      0        0 h2-eth0
```

## Running ryu manager

```bash
ubuntu@sdnhubvm:~[04:45]$ ./ryu/bin/ryu-manager --verbose hojat/Router/rest_router.py
```

* switches configuration
```bash
mininet> s1 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    0      0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1

mininet> s2 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    0      0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1

curl -X POST -d '{"address":"192.168.10.1/24"}' http://localhost:8080/router/0000000000000001
[{"switch_id": "0000000000000001", "command_result": [{"result": "success", "details": "Add address [address_id=1]"}]}]

curl -X POST -d '{"address":"10.10.10.1/24"}' http://localhost:8080/router/000000000100 
[{"switch_id": "0000000000000001", "command_result": [{"result": "success", "details": "Add address [address_id=2]"}]}]


curl -X POST -d '{"address":"192.168.20.1/24"}' http://localhost:8080/router/0000000000000002

curl -X POST -d '{"address":"10.10.10.2/24"}' http://localhost:8080/router/0000000000000002
```

* Now you can see nothing has changed, Everything is just is in the mind of the controller
```bash
mininet> s1 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    0      0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1

mininet> s2 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    0      0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1
```

* Setting static route
```bash
curl -X POST -d '{"destination":"192.168.20.0/24", "gateway":"10.10.10.2"}' http://localhost:8080/router/0000000000000001

curl -X POST -d '{"destination":"192.168.10.0/24", "gateway":"10.10.10.1"}'  http://localhost:8080/router/0000000000000002
```

## Test connections
```bash
mininet> h1 ping h2
PING 192.168.20.10 (192.168.20.10) 56(84) bytes of data.
64 bytes from 192.168.20.10: icmp_seq=1 ttl=62 time=32.8 ms
64 bytes from 192.168.20.10: icmp_seq=2 ttl=62 time=1.84 ms
```

* Looking at flow dump
```bash
 ubuntu@sdnhubvm:~[06:15]$ sudo ovs-ofctl -O OpenFlow13 show s1
OFPT_FEATURES_REPLY (OF1.3) (xid=0x2): dpid:0000000000000001
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS GROUP_STATS QUEUE_STATS
OFPST_PORT_DESC reply (OF1.3) (xid=0x3):
 1(s1-eth1): addr:8e:92:4c:ff:c1:1a
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 2(s1-eth2): addr:aa:2e:11:b0:ae:6c
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 LOCAL(s1): addr:42:d5:af:d7:51:47
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (OF1.3) (xid=0x5): frags=normal miss_send_len=0
ubuntu@sdnhubvm:~[06:15]$ sudo ovs-ofctl -O OpenFlow13 show s2
OFPT_FEATURES_REPLY (OF1.3) (xid=0x2): dpid:0000000000000002
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS GROUP_STATS QUEUE_STATS
OFPST_PORT_DESC reply (OF1.3) (xid=0x3):
 1(s2-eth1): addr:d6:d6:64:2e:0c:91
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 2(s2-eth2): addr:ca:85:e4:91:5c:db
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 LOCAL(s2): addr:aa:84:98:0d:ce:4a
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (OF1.3) (xid=0x5): frags=normal miss_send_len=0

```

* flows
```bash
ubuntu@sdnhubvm:~[06:16]$ sudo ovs-ofctl -O OpenFlow13 dump-flows s1
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x1, duration=1545.634s, table=0, n_packets=0, n_bytes=0, priority=1037,ip,nw_dst=192.168.10.1 actions=CONTROLLER:65535
 cookie=0x2, duration=1462.382s, table=0, n_packets=0, n_bytes=0, priority=1037,ip,nw_dst=10.10.10.1 actions=CONTROLLER:65535
 cookie=0x2, duration=718.229s, table=0, n_packets=0, n_bytes=0, idle_timeout=1800, priority=35,ip,nw_dst=10.10.10.2 actions=dec_ttl,set_field:aa:2e:11:b0:ae:6c->eth_src,set_field:ca:85:e4:91:5c:db->eth_dst,output:2
 cookie=0x1, duration=136.706s, table=0, n_packets=2, n_bytes=196, idle_timeout=1800, priority=35,ip,nw_dst=192.168.10.10 actions=dec_ttl,set_field:8e:92:4c:ff:c1:1a->eth_src,set_field:00:00:00:00:00:01->eth_dst,output:1
 cookie=0x1, duration=1545.634s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=192.168.10.0/24,nw_dst=192.168.10.0/24 actions=NORMAL
 cookie=0x2, duration=1462.380s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=10.10.10.0/24,nw_dst=10.10.10.0/24 actions=NORMAL
 cookie=0x1, duration=1545.634s, table=0, n_packets=1, n_bytes=98, priority=2,ip,nw_dst=192.168.10.0/24 actions=CONTROLLER:65535
 cookie=0x2, duration=1462.388s, table=0, n_packets=0, n_bytes=0, priority=2,ip,nw_dst=10.10.10.0/24 actions=CONTROLLER:65535
 cookie=0x10000, duration=280.542s, table=0, n_packets=2, n_bytes=196, priority=26,ip,nw_dst=192.168.20.0/24 actions=dec_ttl,set_field:aa:2e:11:b0:ae:6c->eth_src,set_field:ca:85:e4:91:5c:db->eth_dst,output:2
 cookie=0x0, duration=2011.215s, table=0, n_packets=10, n_bytes=420, priority=1,arp actions=CONTROLLER:65535
 cookie=0x0, duration=2011.214s, table=0, n_packets=0, n_bytes=0, priority=1,ip actions=drop
 cookie=0x0, duration=2011.214s, table=0, n_packets=0, n_bytes=0, priority=0 actions=NORMAL

ubuntu@sdnhubvm:~[06:16]$ sudo ovs-ofctl -O OpenFlow13 dump-flows s2
OFPST_FLOW reply (OF1.3) (xid=0x2):
 cookie=0x1, duration=779.971s, table=0, n_packets=0, n_bytes=0, priority=1037,ip,nw_dst=192.168.20.1 actions=CONTROLLER:65535
 cookie=0x2, duration=755.610s, table=0, n_packets=0, n_bytes=0, priority=1037,ip,nw_dst=10.10.10.2 actions=CONTROLLER:65535
 cookie=0x2, duration=247.560s, table=0, n_packets=0, n_bytes=0, idle_timeout=1800, priority=35,ip,nw_dst=10.10.10.1 actions=dec_ttl,set_field:ca:85:e4:91:5c:db->eth_src,set_field:aa:2e:11:b0:ae:6c->eth_dst,output:2
 cookie=0x1, duration=175.044s, table=0, n_packets=2, n_bytes=196, idle_timeout=1800, priority=35,ip,nw_dst=192.168.20.10 actions=dec_ttl,set_field:d6:d6:64:2e:0c:91->eth_src,set_field:00:00:00:00:00:02->eth_dst,output:1
 cookie=0x1, duration=779.970s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=192.168.20.0/24,nw_dst=192.168.20.0/24 actions=NORMAL
 cookie=0x2, duration=755.609s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=10.10.10.0/24,nw_dst=10.10.10.0/24 actions=NORMAL
 cookie=0x1, duration=779.972s, table=0, n_packets=1, n_bytes=98, priority=2,ip,nw_dst=192.168.20.0/24 actions=CONTROLLER:65535
 cookie=0x2, duration=755.612s, table=0, n_packets=0, n_bytes=0, priority=2,ip,nw_dst=10.10.10.0/24 actions=CONTROLLER:65535
 cookie=0x10000, duration=231.378s, table=0, n_packets=2, n_bytes=196, priority=26,ip,nw_dst=192.168.10.0/24 actions=dec_ttl,set_field:ca:85:e4:91:5c:db->eth_src,set_field:aa:2e:11:b0:ae:6c->eth_dst,output:2
 cookie=0x0, duration=2048.583s, table=0, n_packets=7, n_bytes=294, priority=1,arp actions=CONTROLLER:65535
 cookie=0x0, duration=2048.583s, table=0, n_packets=0, n_bytes=0, priority=1,ip actions=drop
 cookie=0x0, duration=2048.583s, table=0, n_packets=0, n_bytes=0, priority=0 actions=NORMAL


```

* NO new route has added and everything is on the controller
```bash
mininet> s1 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    0      0        0 eth0
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1

sudo ovs-ofctl -O OpenFlow13 show s1

sudo ovs-ofctl -O OpenFlow13 dump-flows s1
```