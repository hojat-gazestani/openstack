https://docs.openstack.org/neutron/victoria/admin/deploy-ovs-selfservice.html

### Network - openvswitch - self service - Controller Node
```shell

sudo apt install ovs layer2-agent layer3-agent ovs

sudo vim neutron.conf 
[DEFAULT]
service_plugins = router
allow_overlapping_ips = True

sudo vim ml2_conf.ini
[ml2]
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = openvswitch,l2population

[ml2_type_vxlan]
vni_ranges = VNI_START:VNI_END

sudo systemctl neutrom-server ovs-agent

```
### Network node
```shell

sudo apt install ovs layer2-agent layer3-agent

sudo vim neutron.conf
[DEFAULT]
core_plugin = ml2
auth_strategy = keystone

[database]
# ...

[keystone_authtoken]
# ...

[nova]
# ...

[agent]
# ...

sudo systemctl start ovs

$ ovs-vsctl add-br br-provider
$ ovs-vsctl add-port br-provider PROVIDER_INTERFACE

sudo vim openvswitch_agent.ini 
[ovs]
bridge_mappings = provider:br-provider
local_ip = OVERLAY_INTERFACE_IP_ADDRESS

[agent]
tunnel_types = vxlan
l2_population = True

[securitygroup]
firewall_driver = iptables_hybrid

sudo vim l3_agent.ini
[DEFAULT]
interface_driver = openvswitch

sudo systemctl start ovs-agnet layer3-agnet

```
### Compute nodes
```shell

sudo vim openvswitch_agent.ini
[ovs]
local_ip = OVERLAY_INTERFACE_IP_ADDRESS

[agent]
tunnel_types = vxlan
l2_population = True

sudo systemctl restart ovs-agent

```

### Verify service operation
```shell
. admin-openrc
openstack network agent list

```

### Create initial networks - Controller
```shell

. admin-openrc
openstack network set --external provider1

. demo-openrc
openstack network create selfservice1
openstack subnet create --subnet-range 192.0.2.0/24 \
  --network selfservice1 --dns-nameserver 8.8.4.4 selfservice1-v4
openstack subnet create --subnet-range fd00:192:0:2::/64 --ip-version 6 \
  --ipv6-ra-mode slaac --ipv6-address-mode slaac --network selfservice1 \
  --dns-nameserver 2001:4860:4860::8844 selfservice1-v6


openstack router create router1
openstack router add subnet router1 selfservice1-v4
openstack router add subnet router1 selfservice1-v6

openstack router set --external-gateway provider1 router1

```
### Verify network operation
```shell

ip netns

. demo-openrc
openstack security group rule create --proto icmp default
openstack security group rule create --ethertype IPv6 --proto ipv6-icmp default
openstack security group rule create --proto tcp --dst-port 22 default
openstack security group rule create --ethertype IPv6 --proto tcp --dst-port 22 default

openstack server create --flavor 1 --image cirros --nic net-id=NETWORK_ID selfservice-instance1

openstack server list

ping6 -c 4 fd00:192:0:2:f816:3eff:fe30:9cb0

openstack floating ip create provider1
openstack server add floating ip selfservice-instance1 203.0.113.16

ping -c 4 203.0.113.16

```