## Compute - nova
```shell
sudo mysql

CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;

GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'PASS';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' \
  IDENTIFIED BY 'PASS';

GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'PASS';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' \
  IDENTIFIED BY 'PASS';

GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'PASS';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' \
  IDENTIFIED BY 'PASS';
```

```shell
. admin-openrc

openstack user create --domain default --password-prompt nova

openstack role add --project service --user nova admin

openstack service create --name nova \
  --description "OpenStack Compute" compute


openstack endpoint create --region RegionOne \
  compute public http://controller:8774/v2.1
openstack endpoint create --region RegionOne \
  compute internal http://controller:8774/v2.1
openstack endpoint create --region RegionOne \
  compute admin http://controller:8774/v2.1

openstack user create --domain default --password-prompt placement

openstack role add --project service --user placement admin

openstack service create --name placement --description "Placement API" placement

openstack endpoint create --region RegionOne placement public http://controller:8778
openstack endpoint create --region RegionOne placement internal http://controller:8778
openstack endpoint create --region RegionOne placement admin http://controller:8778

```

### Install and configure components
```shell
sudo apt install nova-api nova-conductor nova-consoleauth \
  nova-novncproxy nova-scheduler nova-placement-api

sudo vim /etc/nova/nova.conf
[DEFAULT]
transport_url = rabbit://openstack:PASS@controller
my_ip = 10.0.0.11
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver


[api_database]
connection = mysql+pymysql://nova:PASS@controller/nova_api

[database]
connection = mysql+pymysql://nova:PASS@controller/nova

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
password = PASS

[vnc]
enabled = true
# ...
server_listen = $my_ip
server_proxyclient_address = $my_ip

[glance]
# ...
api_servers = http://controller:9292

[oslo_concurrency]
# ...
lock_path = /var/lib/nova/tmp

[placement]
# ...
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller:5000/v3
username = placement
password = PASS

[scheduler]
discover_hosts_in_cells_interval = 300
```

```shell
sudo su -s /bin/sh -c "nova-manage api_db sync" nova

sudo su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova

sudo su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova

sudo su -s /bin/sh -c "nova-manage db sync" nova
```

### Verify
```shell
nova-manage cell_v2 list_cells
```

### Finalize installation
```shell
service nova-api restart
service nova-consoleauth restart
service nova-scheduler restart
service nova-conductor restart
service nova-novncproxy restart
```