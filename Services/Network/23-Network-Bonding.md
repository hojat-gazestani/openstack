# Link Aggregation Between Cisco and Ubuntu

## Table of Contents
1. [Cisco IOS Switch LACP Configuration](#cisco-ios-switch-lacp-configuration)
2. [Linux Traditional Bonding](#linux-traditional-bonding)
   - [Installation](#installation)
   - [Ensure Kernel Support](#ensure-kernel-support)
   - [Traditional Network Configuration](#traditional-network-configuration)
   - [Testing](#testing)
   - [VLAN Configuration](#linux-vlan-configuration)
3. [Linux Netplan Bonding](#linux-netplan-bonding)
4. [Open vSwitch Bonding](#open-vSwitch-bonding)
5. [Bonding modes descriptions](#bonding-modes-descriptions)


## Cisco IOS Switch LACP Configuration

To configure LACP on a Cisco IOS switch, use the following commands:

```shell
interface Port-channel2
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 1,2
 switchport mode trunk
 spanning-tree portfast trunk

interface GigabitEthernet1/0/23
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 1,51
 spanning-tree portfast trunk
 channel-group 2 mode active

interface GigabitEthernet1/0/24
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 1,51
 spanning-tree portfast trunk
 channel-group 2 mode active
```

## Linux Traditional Bonding

### Installation

Install necessary packages for bonding and VLANs:

```shell
sudo apt-get install ifenslave net-tools -y
```

### Ensure kernel support
Add necessary modules to `/etc/modules` and load the bonding module:
```shell
sudo vi /etc/modules
bonding

sudo modprobe bonding
```

Create or modify `/etc/modprobe.d/bonding.conf` to set bonding parameters:
```sh
# /etc/modprobe.d/bonding.conf
bonding mode=4 miimon=100 lacp_rate=1
```

#### Traditional Network Configuration
* Manual Bonding Setup
Configure bonding manually:

```shell
sudo ip link add bond0 type bond mode 802.3ad
sudo ip link set eno1 master bond0
sudo ip link set eno2 master bond0
```

* Active-Backup Setup

For active-backup bonding, configure as follows:

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

* IEEE 802.3ad LACP Bonding Protocol
For LACP bonding:
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

### Testing
Verify the bonding configuration and test connectivity:
```shell
cat /proc/net/bonding/bond1

speedometer -r bond0 -t bond0

iperf -s
iperf -c 192.168.1.8
```

### VLAN Configuration
Configure VLANs and bridges:
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
     
auto bond1.240
iface bond1.240 inet manual

auto br-vxlan
iface br-vxlan inet static
        address 172.29.240.15
        netmask 255.255.255.0
        bridge_ports bond1.240
        bridge_stp off
        
auto br-vlan
iface br-vlan inet manual
        bridge_ports bond1
        bridge_stp off
  
sudo ifup enp1s0.10

sudo ip addr add 192.168.100.2/24 dev enp1s0.100
```

## Linux Netplan Bonding
For Ubuntu 22.04, use Netplan to configure bonding:

1. Load the Bonding Kernel Module:

```sh
#  Load the Bonding Kernel Module
sudo modprobe bonding
```
2. Ensure the Bonding Module Loads at Boot:
```sh
# Ensure the Bonding Module Loads at Boot
echo "bonding" | sudo tee -a /etc/modules
```

3. Verify the Bonding Module is Loaded:
```sh
# Verify the Bonding Module is Loaded
lsmod | grep bonding
```

4. Create a Netplan Configuration File:
```sh
# Create a Netplan Configuration File
sudo vim /etc/netplan/01-bondcfg.yaml
```

Example configuration:
```sh
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      dhcp4: no
    eno2:
      dhcp4: no
  bonds:
    bond0:
      interfaces:
        - eno1
        - eno2
      parameters:
        mode: 802.3ad
        lacp-rate: fast
        mii-monitor-interval: 100
      addresses:
        - 172.27.103.102/24
      routes:
        - to: default
          via: 172.27.103.1
      nameservers:
        addresses:
          - 172.22.22.22
```
5. Apply Netplan Configuration:
```sh
sudo netplan apply
```

6. Verify Bonding Configuration:
```sh
cat /proc/net/bonding/bond0
```

## Open vSwitch Bonding

### Installing Open vSwitch

To install Open vSwitch on Ubuntu 22.04:

1. Update the System:

```sh
sudo apt update -y
sudo apt upgrade -y
```

2. Install Open vSwitch:
```sh
sudo apt install openvswitch-switch -y
```

3. Verify the Installation: Check if the Open vSwitch service is running:
```sh
sudo systemctl status openvswitch-switch
```

4. Create a Bridge: After installing, you can create a new OVS bridge using:
```sh
sudo ovs-vsctl add-br br0
```

5. Add a Port to the Bridge: You can add a network interface to the bridge:
```sh
sudo ovs-vsctl add-port br0 eth0
```

6. Check the Bridge Configuration: View the current configuration with:
```sh
sudo ovs-vsctl show
```

### Tshoot
* List All Bridges:
```sh
sudo ovs-vsctl list-br
```

* Delete a Bridge:
```sh
sudo ovs-vsctl del-br br0
```

* List Ports on a Bridge:
```sh
sudo ovs-vsctl list-ports br0
```


## Bonding modes descriptions

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

[Didn't use it](https://access.redhat.com/solutions/3417681)