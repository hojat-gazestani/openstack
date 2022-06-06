## Compute - nova
```shell
sudo apt install nova-compute -y
```

```shell
sudo vim /etc/nova/nova.conf 
[DEFAULT]
# remove the log_dir option
transport_url = rabbit://openstack:RABBIT_PASS@controller
my_ip = MANAGEMENT_INTERFACE_IP_ADDRESS
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver

[api]
auth_strategy = keystone

[keystone_authtoken]
auth_url = http://controller:5000/v3
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = NOVA_PASS

[vnc]
enabled = True
server_listen = 0.0.0.0
server_proxyclient_address = $my_ip
novncproxy_base_url = http://controller:6080/vnc_auto.html

[glance]
api_servers = http://controller:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller:5000/v3
username = placement
password = PLACEMENT_PASS
```

### Finalize installation
```shell
egrep -c '(vmx|svm)' /proc/cpuinfo

sudo vim /etc/nova/nova-compute.conf 
[libvirt]
# ...
virt_type = qemu
```

```shell
sudo service nova-compute restart
```

### Verify
```shell
```

## Controller

```shell
. admin-openrc

openstack compute service list --service nova-compute

sudo su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
```