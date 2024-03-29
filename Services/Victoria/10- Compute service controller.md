## Compute service

### controller

```shell
sudo mysql

CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;

GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' \
  IDENTIFIED BY 'openstack';

GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' \
  IDENTIFIED BY 'openstack';

GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' \
  IDENTIFIED BY 'openstack';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' \
  IDENTIFIED BY 'openstack';

. admin-openrc

openstack user create --domain default --password-prompt nova

openstack role add --project service --user nova admin


openstack service create --name nova \
  --description "OpenStack Compute" compute


openstack endpoint create --region RegionOne \
  compute public http://controller01:8774/v2.1
openstack endpoint create --region RegionOne \
  compute internal http://controller01:8774/v2.1
openstack endpoint create --region RegionOne \
  compute admin http://controller01:8774/v2.1


sudo apt install nova-api nova-conductor nova-novncproxy nova-scheduler -y

sudo vim /etc/nova/nova.conf

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01:5672/
my_ip = 192.168.57.50

[api_database]
connection = mysql+pymysql://nova:openstack@controller01/nova_api

[database]
connection = mysql+pymysql://nova:openstack@controller01/nova

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
server_listen = $my_ip
server_proxyclient_address = $my_ip
## OR
[vnc]
enabled = false
[spice]
agent_enabled = False
enabled = True
html5proxy_base_url = http://controller01:6082/spice_auto.html
html5proxy_host = 0.0.0.0
html5proxy_port = 6082
keymap = en-us
server_listen = 127.0.0.1
server_proxyclient_address = 127.0.0.1

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

sudo su -s /bin/sh -c "nova-manage api_db sync" nova

sudo su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
#sudo su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --transport-url rabbit://openstack:****@controller01:5672/ --database_connection mysql+pymysql://nova:****@controller01/nova  --verbose" nova 
sudo  su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova

sudo su -s /bin/sh -c "nova-manage db sync" nova

sudo su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova



sudo service nova-api restart
sudo service nova-scheduler restart
sudo service nova-conductor restart
sudo service nova-novncproxy restart

```

### nova troubleshooting

```shell
sudo su -s /bin/sh -c "nova-manage cell_v2 delete_cell --cell_uuid  00000000-0000-0000-0000-000000000000" nova

sudo su -s /bin/sh -c "nova-manage api_db sync" nova

sudo su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
sudo  su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova

sudo su -s /bin/sh -c "nova-manage db sync" nova
sudo su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova

openstack compute service list --service nova-compute
```