## OVSK

```bash
sudo mn --mac --switch ovsk --controller remote -x

sudo ovs-vsctl list-br
s1

sudo ovs-vsctl list-ports s1
s1-eth1
s1-eth2

sudo ovs-vsctl add-br s2
sudo ovs-vsctl list-br
s1
s2

sudo ovs-vsctl list-ports s2
# Nothing, because we have not add any ports
```

* Mininet is unaware of s2
```bash
mininet> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0
c0
```

* But we can see on OVSK
```bash
sudo ovs-vsctl show
873c293e-912d-4067-82ad-d1116d2ad39f
    Bridge "s2"
        Port "s2"
            Interface "s2"
                type: internal
    Bridge "s1"
        Controller "tcp:127.0.0.1:6633"
        Controller "ptcp:6634"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
    ovs_version: "2.3.90"
```

```bash
sudo ovs-vsctl set Bridge s2 protocol=OpenFlow13
sudo ovs-vsctl set-controller s2 ssl:127.0.0.1:6636
sudo ovs-vsctl show
873c293e-912d-4067-82ad-d1116d2ad39f
    Bridge "s2"
        Controller "ssl:127.0.0.1:6636"
        Port "s2"
            Interface "s2"
                type: internal
    Bridge "s1"
        Controller "tcp:127.0.0.1:6633"
        Controller "ptcp:6634"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
    ovs_version: "2.3.90"
```

```bash
sudo ovs-ofctl dump-flows s1
NXST_FLOW reply (xid=0x4):

```