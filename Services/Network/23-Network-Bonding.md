Link aggregation between Cisco and Ubuntu
=========================================

Cisco IOS switch LACP configuration
-----------------------------------
```shell
interface Port-channel2
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 1,2
 switchport mode trunk
 spanning-tree portfast trunk

interface GigabitEthernet1/0/23
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 2 mode active

interface GigabitEthernet1/0/24
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 2 mode active
```

linux
-----
### Installation
```shell
sudo apt-get install ifenslave
```

### Ensure kernel support
```shell
sudo vi /etc/modules
loop
lp
rtc
bonding

sudo modprobe bonding

# /etc/modprobe.d/bonding.conf
bonding mode=4 miimon=100 lacp_rate=1
```

#### Linux Network Configuration
* Manual
```shell
sudo ip link add bond0 type bond mode 802.3ad
sudo ip link set eno1 master bond0
sudo ip link set eno2 master bond0
```

* active-backup setup,
```shell
auto eno1
iface eno1 inet manual
    bond-master bond0
    bond-primary eno1

auto eno2
iface eno2 inet manual
    bond-master bond0

auto bond0
iface bond0 inet manual
    address 192.168.1.10
    gateway 192.168.1.1
    netmask 255.255.255.0
    bond-mode active-backup
    bond-miimon 100
    bond-slaves none
```

* IEEE 802.3ad LACP bonding protocol
```shell
sudo vim /etc/network/interfaces  
auto eno3
iface eno3 inet manual
    bond-master bond0
 
auto eno4
iface eno4 inet manual
     bond-master bond0
 
auto bond0
iface bond0 inet manual
     address 10.0.0.80
     gateway 10.0.0.1
     netmask 255.255.255.0
     bond-mode 802.3ad 
     bond-miimon 100
     bond-lacp-rate 1
     bond-slaves none
```

### test
```shell
cat /proc/net/bonding/bond1
```

```shell
speedometer -r bond0 -t bond0

iperf -s
iperf -c 192.168.1.8
```

### linux vlan
```shell
sudo apt-get install vlan
sudo modprobe 8021q
modinfo 8021q

sudo vconfig add eno1 52

sudo vim /etc/network/interfaces
auto enp1s0.10
iface enp1s0.10 inet dhcp
  vlan-raw-device enp1s0
  
auto eno1.52
iface eno1.52 inet static
     address 172.20.52.196
     netmask 255.255.255.0
     
  
sudo ifup enp1s0.10

sudo ip addr add 192.168.100.2/24 dev enp1s0.100
```

## Descriptions

### bonding modes
* Mode 0, balance-rr
  * Round-robin
* Mode 1, active-backup
* Mode 3, broadcast
  * provides fault tolerance
* Mode 4, 802.3ad
  * LACP
  * Creates aggregation groups that share the same speed and duplex settings. 
  1. Ethtool support in the base drivers for retrieving the speed and duplex of each slave. 
  2. A switch that supports IEEE 802.3ad Dynamic link aggregation. Most switches will require some type of configuration to enable 802.3ad mode.
* Mode 5, balance-tlb
  * Adaptive transmit load balancing: 
* Mode 6, balance-alb
  * Adaptive load balancing:



* Mode 2, balance-xor
  * balancing algorithm modes
    * Possible values are:

layer2 Uses XOR of hardware MAC addresses to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave.

layer2+3 Uses XOR of hardware MAC addresses and IP addresses to generate the hash. This algorithm will place all traffic to a particular network peer on the same slave.

layer3+4 This policy uses upper layer protocol information, when available, to generate the hash. This allows for traffic to a particular network peer to span multiple slaves, although a single connection will not span multiple slaves.

encap2+3 This policy uses the same formula as layer2+3 but it relies on skb_flow_dissect to obtain the header fields which might result in the use of inner headers if an encapsulation protocol is used.

encap3+4 This policy uses the same formula as layer3+4 but it relies on skb_flow_dissect to obtain the header fields which might result in the use of inner headers if an encapsulation protocol is used.

The default value is layer2. This option was added in bonding version 2.6.3. In earlier versions of bonding, this parameter does not exist, and the layer2 policy is the only policy. The layer2+3 value was added for bonding version 3.2.2. 
