Link aggregation between Cisco and Ubuntu
=========================================

### Cisco IOS switch LACP configuration
```shell
interface Port-channel2
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 1,2
 switchport mode trunk
 spanning-tree portfast trunk
!
interface GigabitEthernet1/0/23
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 2 mode active
!
interface GigabitEthernet1/0/24
 switchport trunk encapsulation dot1q
 switchport mode trunk
 channel-group 2 mode active
!
```

### Debian Kernel Module Configuration
#### Ubuntu Kernel Module Configuration
```shell
# /etc/modprobe.d/bonding.conf
 
bonding mode=4 miimon=100 lacp_rate=1
```

#### Linux Network Configuration

#### Debian / Ubuntu Network Setup
```shell
sudo apt-get install ifenslave

sudo vim /etc/network/interfaces  
auto eno3
    iface eno3 inet manual
    bond-master bond0
 
auto eno4
     iface eno4 inet manual
     bond-master bond0
 
auto bond0
     iface bond0 inet static
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
