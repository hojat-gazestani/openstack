* https://docs.openstack.org/nova/victoria/install/compute-install-ubuntu.html

##compute service

### compute node

```shell
sudo apt install nova-compute -y

sudo vim /etc/nova/nova.conf
[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
my_ip = 192.168.57.51

[api]
auth_strategy = keystone

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000/
auth_url = http://controller01:5000/
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = openstack

[vnc]
enabled = true
server_listen = 0.0.0.0
server_proxyclient_address = $my_ip
novncproxy_base_url = http://controller01:6080/vnc_auto.html

[glance]
api_servers = http://controller01:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller01:5000/v3
username = placement
password = openstack

[scheduler]
discover_hosts_in_cells_interval = 300
```

### Finalize installation

```shell
egrep -c '(vmx|svm)' /proc/cpuinfo

sudo vim /etc/nova/nova-compute.conf 
[libvirt]
virt_type = qemu

sudo service nova-compute restart
```

### Add the compute node to the cell database 

```shell
. admin-openrc
openstack compute service list --service nova-compute

sudo su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
```

### Tshout
```shell
mysql -u nova -h controller01 -popenstack
```
