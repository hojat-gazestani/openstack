https://docs.openstack.org/neutron/victoria/admin/deploy-ovs-provider.html

## network - Open vSwitch - provider on contorller node
```shell

sudo apt install neutron-server ml2-plugin

sudo vim /etc/neutron/neutron.conf
[DEFAULT]
core_plugin = ml2
auth_strategy = keystone
service_plugins =
dhcp_agents_per_network = 2


[database]
# ...

[keystone_authtoken]
# ...

[nova]
# ...

[agent]
# ...

sudo vim /etc/neutron/plugins/ml2/ml2_conf.ini 
[ml2]
type_drivers = flat,vlan
tenant_network_types =
mechanism_drivers = openvswitch
extension_drivers = port_security

[ml2_type_flat]
flat_networks = provider

[ml2_type_vlan]
network_vlan_ranges = provider

sudo su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

```

### Configure the Compute service to use the Networking service
```shell

sudo vim /etc/nova/nova.conf
[neutron]
auth_url = http://controller01:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = openstack
service_metadata_proxy = true
metadata_proxy_shared_secret = openstack

```
### Compute nodes
```shell

sudo apt install ovs layer2 agent dhcp-agent metadata-agent ovs
sudo apt install openvswitch-switch neutron-openvswitch-agent neutron-dhcp-agent neutron-metadata-agent -y

sudo vim /etc/neutron/neutron.conf
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

sudo vim /etc/neutron/plugins/ml2/openvswitch_agent.ini
[ovs]
bridge_mappings = provider:br-provider

[securitygroup]
firewall_driver = iptables_hybrid

sudo vim /etc/neutron/dhcp_agent.ini
[DEFAULT]
interface_driver = openvswitch
enable_isolated_metadata = True
force_metadata = True

sudo vim /etc/neutron/metadata_agent.ini
[DEFAULT]
nova_metadata_host = controller
metadata_proxy_shared_secret = openstack

```
### Configure the Compute service to use the Networking service
```shell
sudo vim /etc/nova/nova.conf
[neutron]
auth_url = http://controller01:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = openstack
service_metadata_proxy = true
metadata_proxy_shared_secret = openstack

sudo systemctl restart openvswitch-switch.service

ovs-vsctl add-br br-provider
ovs-vsctl add-port br-provider PROVIDER_INTERFACE

sudo systemctl start ovs-agent dhcp-agent metadata-agent

```

### Verify service operation
```shell
. admin-openrc
openstack network agent list

```
### Create initial networks
```shell

. admin-openrc

openstack network create --share --provider-physical-network provider \
  --provider-network-type flat provider1

openstack subnet create --subnet-range 203.0.113.0/24 --gateway 203.0.113.1 \
  --network provider1 --allocation-pool start=203.0.113.11,end=203.0.113.250 \
  --dns-nameserver 8.8.4.4 provider1-v4

openstack subnet create --subnet-range fd00:203:0:113::/64 --gateway fd00:203:0:113::1 \
  --ip-version 6 --ipv6-address-mode slaac --network provider1 \
  --dns-nameserver 2001:4860:4860::8844 provider1-v6

```
### Verify network operation
```shell

ip netns
openstack security group rule create --proto icmp default
openstack security group rule create --ethertype IPv6 --proto ipv6-icmp default
openstack security group rule create --proto tcp --dst-port 22 default
openstack security group rule create --ethertype IPv6 --proto tcp --dst-port 22 default

openstack server create --flavor 1 --image cirros \
  --nic net-id=NETWORK_ID provider-instance1

openstack server list

ping -c 4 203.0.113.13

ping6 -c 4 fd00:203:0:113:f816:3eff:fe58:be4e

```