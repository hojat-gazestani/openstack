## Networking service Installation Guide - Compute Node
```shell

sudo apt install neutron-linuxbridge-agent

sudo vim /etc/neutron/neutron.conf 
[DEFAULT]
auth_strategy = keystone
transport_url = rabbit://openstack:openstack@controller01

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = openstack

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp

```

### Provider networks
```shell

sudo vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:ens192

[vxlan]
enable_vxlan = false

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

sudo sysctl net.bridge.bridge-nf-call-iptables
sudo sysctl net.bridge.bridge-nf-call-ip6tables

```

### Self-service networks
```shell

sudo vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:ens192

[vxlan]
enable_vxlan = true
local_ip = 192.168.52.52
l2_population = true

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

sudo sysctl net.bridge.bridge-nf-call-iptables
sudo sysctl net.bridge.bridge-nf-call-ip6tables
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

sudo service nova-compute restart
sudo service neutron-linuxbridge-agent restart

```
### Verify operation
```shell
. admin-openrc
openstack extension list --network

openstack network agent list
```