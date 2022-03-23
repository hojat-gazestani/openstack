## Compute - Network - Neutron

```shell
sudo apt install neutron-linuxbridge-agent

```

```shell
sudo vim  /etc/neutron/neutron.conf
[DEFAULT]
# ...
transport_url = rabbit://openstack:RABBIT_PASS@controller
auth_strategy = keystone

[keystone_authtoken]
# ...
auth_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = NEUTRON_PASS

[oslo_concurrency]
# ...
lock_path = /var/lib/neutron/tmp
````

### Provider networks

* Configure the Linux bridge agent
```shell
sudo vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:PROVIDER_INTERFACE_NAME

[vxlan]
enable_vxlan = false

[securitygroup]
# ...
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
````

```shell
net.bridge.bridge-nf-call-iptables
net.bridge.bridge-nf-call-ip6tables
````

### Self-service networks

```shell
sudo vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:PROVIDER_INTERFACE_NAME


[vxlan]
enable_vxlan = true
local_ip = OVERLAY_INTERFACE_IP_ADDRESS
l2_population = true

[securitygroup]
# ...
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver


````

```shell
net.bridge.bridge-nf-call-iptables
net.bridge.bridge-nf-call-ip6tables
```

### Configure the Compute service to use the Networking service

```shell
sudo vim /etc/nova/nova.conf

[neutron]
# ...
url = http://controller:9696
auth_url = http://controller:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = NEUTRON_PASS


````

### Finalize installation

```shell
sudo service nova-compute restart
sudo service neutron-linuxbridge-agent restart
````